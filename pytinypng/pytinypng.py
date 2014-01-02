import os
import time
import argparse
from os.path import realpath
from collections import defaultdict
from domain import TinyPNGError
from api import shrink
from handlers import ScreenHandler
from utils import files_with_exts, target_path

TINYPNG_SLEEP_SEC = 1

class StopProcessing(Exception): pass
class RetryProcessing(Exception): pass


def _process_file(input_file, output_file, apikey, callback=None):
    bytes = open(input_file, 'rb').read()
    compressed = shrink(bytes, apikey)
    if callback:
        callback(compressed, input_file=input_file)

    if compressed.success and compressed.bytes:
        open(output_file, 'wb+').write(compressed.bytes)
    else:
        if compressed.errno in (TinyPNGError.Unauthorized, TinyPNGError.TooManyRequests):
            raise StopProcessing()
        if compressed.errno == TinyPNGError.InternalServerError:
            raise RetryProcessing()

    return compressed


def process_directory(source, dest, apikey, handler, allow_overwrite=False):
    """
    @type: handler: Handler
    """

    handler.on_start()

    attempts = defaultdict(lambda: 0)
    input_files = files_with_exts(source, suffix='.png')
    next_ = lambda: next(input_files, None)

    current_file = next_()

    while current_file:
        dirname, basename, output_file = target_path(source, dest, current_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif os.path.exists(output_file) and not allow_overwrite:
            handler.on_skip(current_file)
            current_file = next_()
            continue

        try:
            handler.on_pre_item(current_file)
            _process_file(current_file, output_file, apikey, handler.on_post_item)
            current_file = next_()
        except StopProcessing:
            break
        except RetryProcessing:
            handler.on_retry(current_file)
            time.sleep(TINYPNG_SLEEP_SEC)
            if attempts[current_file] < 9:
                attempts[current_file] += 1
            else:
                current_file = next_()

    handler.on_finish()


def main(args):
    input_dir = realpath(args.input)

    if not args.output:
        output_dir = input_dir + "-output"
    else:
        output_dir = realpath(args.output)

    handler = ScreenHandler()

    try:
        process_directory(input_dir, output_dir, args.apikey, handler)
    except KeyboardInterrupt:
        handler.on_finish()


if __name__ == '__main__':
    """TODO:
    add support for allow overwrite
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input',
                        metavar='INPUT',
                        help='Input directory with PNG files')
    parser.add_argument('output', nargs='?',
                        metavar='OUTPUT',
                        help='Output directory')
    parser.add_argument('--apikey',
                        metavar='APIKEY',
                        default=os.environ.get('TINYPNG_APIKEY'),
                        help='TinyPNG API Key')

    args = parser.parse_args()
    main(args)
