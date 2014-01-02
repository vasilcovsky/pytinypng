import os
import time
import argparse
from os.path import realpath
from collections import defaultdict
from domain import TinyPNGError, FATAL_ERRORS
from api import shrink
from handlers import ScreenHandler
from utils import files_with_exts, target_path, write_binary, read_binary, find_apikey


TINYPNG_SLEEP_SEC = 1


class RetryProcessing(Exception):
    def __init__(self, response):
        self._response = response

    @property
    def response(self):
        return self._response


class StopProcessing(RetryProcessing):
    pass


def _process_file(input_file, output_file, apikey):
    bytes_ = read_binary(input_file)
    compressed = shrink(bytes_, apikey)

    if compressed.success and compressed.bytes:
        write_binary(output_file, compressed.bytes)
    else:
        if compressed.errno in FATAL_ERRORS:
            raise StopProcessing(compressed)
        elif compressed.errno == TinyPNGError.InternalServerError:
            raise RetryProcessing(compressed)

    return compressed


def process_directory(source, dest, apikey, handler, overwrite=False):
    """
    @type: handler: Handler
    """

    handler.on_start()

    attempts = defaultdict(lambda: 0)
    input_files = files_with_exts(source, suffix='.png')
    next_ = lambda: next(input_files, None)

    current_file = next_()
    response = None
    last_processed = None

    while current_file:
        output_file = target_path(source, dest, current_file)

        if os.path.exists(output_file) and not overwrite:
            handler.on_skip(current_file)
            current_file = next_()
            continue

        try:
            handler.on_pre_item(current_file)

            last_processed = current_file

            response = _process_file(current_file, output_file, apikey)
            current_file = next_()

        except StopProcessing as e:
            response = e.response
            handler.on_stop(response.errmsg)
            break
        except RetryProcessing as e:
            response = e.response
            handler.on_retry(current_file)
            time.sleep(TINYPNG_SLEEP_SEC)

            if attempts[current_file] < 9:
                attempts[current_file] += 1
            else:
                current_file = next_()
        finally:
            handler.on_post_item(response, last_processed)

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
                        default=find_apikey(),
                        help='TinyPNG API Key')

    args = parser.parse_args()
    main(args)
