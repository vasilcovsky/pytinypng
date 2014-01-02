import os
import time
import argparse
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
    input_file = next(input_files, None)

    while input_file:
        dirname, basename, output_file = target_path(source, dest, input_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif os.path.exists(output_file) and not allow_overwrite:
            handler.on_skip(input_file)
            input_file = next(input_files, None)
            continue

        try:
            handler.on_pre_item(input_file)
            _process_file(input_file, output_file, apikey, handler.on_post_item)
            input_file = next(input_files, None)
        except StopProcessing:
            break
        except RetryProcessing:
            handler.on_retry(input_file)
            time.sleep(TINYPNG_SLEEP_SEC)
            if attempts[input_file] < 9:
                attempts[input_file] += 1
            else:
                input_file = next(input_files, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('apikey',
                        metavar='APIKEY',
                        help='TinyPNG API Key')
    parser.add_argument('input',
                        metavar='INPUT',
                        help='Input directory with PNG files')
    parser.add_argument('output',
                        metavar='OUTPUT',
                        help='Output directory')

    args = parser.parse_args()

    input_dir = os.path.realpath(args.input)
    output_dir = os.path.relpath(args.output)

    handler = ScreenHandler()

    try:
        process_directory(input_dir, output_dir, args.apikey, handler)
    except KeyboardInterrupt:
        pass