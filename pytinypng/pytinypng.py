import os
import time
import argparse
from collections import defaultdict
from domain import TinyPNGError
from api import shrink
from utils import files_with_exts, target_path
import screen

TINYPNG_SLEEP_SEC = 1

class StopProcessing(Exception):
    pass

class RetryProcessing(Exception):
    pass


def tinypng_process_directory(source, dest, apikey,
                              item_callback=None, begin_callback=None, retry_callback=None):
    def process_file(input_file):
        bytes_ = open(input_file, 'rb').read()
        compressed = shrink(bytes_, apikey, filename=input_file)
        if item_callback:
            item_callback(compressed)

        if compressed.success and compressed.bytes:
            target_dir, filename = target_path(source, dest, input_file)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            open(os.path.join(target_dir, filename), 'wb+').write(compressed.bytes)
        else:
            if compressed.errno in (TinyPNGError.Unauthorized, TinyPNGError.TooManyRequests):
                raise StopProcessing()
            if compressed.errno == TinyPNGError.InternalServerError:
                raise RetryProcessing()

        return compressed

    if begin_callback:
        begin_callback()

    attempts = defaultdict(lambda: 0)
    input_files = files_with_exts(source, suffix='.png')
    input_file = next(input_files, None)

    while input_file:
        try:
            process_file(input_file)
            input_file = next(input_files, None)
        except StopProcessing:
            break
        except RetryProcessing:
            if retry_callback:
                retry_callback()
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

    tinypng_process_directory(input_dir, output_dir, args.apikey,
                              item_callback=screen.item_row,
                              begin_callback=screen.table_header)
