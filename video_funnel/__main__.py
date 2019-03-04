import asyncio
import re
from argparse import ArgumentParser

from .server import serve


def convert_unit(s):
    num, unit = re.match(r'(\d+)([BKMG]?)', s, re.I).groups()
    units = {'B': 1, 'K': 1024, 'M': 1024 * 1024, 'G': 1024 * 1024 * 1024}
    return int(num) * units[unit.upper() or 'B']


def make_args():
    ap = ArgumentParser(
        description='Video Funnel -- Use multiple connections to request the '
        'video, then feed the combined data to the player.')

    ap.add_argument('url', metavar='URL', help='the video url')
    ap.add_argument('--port', type=int, default=2345, help='port to listen')
    ap.add_argument(
        '--block-size',
        '-b',
        metavar='N',
        type=convert_unit,
        default='4M',
        help='size of one block')
    ap.add_argument(
        '--piece-size',
        '-p',
        metavar='N',
        type=convert_unit,
        default='1M',
        help='size of one piece')
    ap.add_argument(
        '--max-tries',
        '-r',
        type=int,
        metavar='N',
        default=10,
        help='Limit retries on network errors.')
    ap.add_argument(
        '--load-cookies',
        '-c',
        choices=['chrome', 'chromium', 'firefox'],
        help='load browser cookies')
    ap.add_argument(
        '--original-url',
        '-g',
        action='store_true',
        help='always use the original URL '
        '(no optimization for 3XX response code)')

    return ap.parse_args()


try:
    asyncio.run(serve(make_args()))
except KeyboardInterrupt:
    pass
