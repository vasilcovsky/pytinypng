import os
import time
import glob
import json
import argparse
from collections import defaultdict
from utils import Enum
from base64 import b64encode
from pytinypng.response import TinyPNGResponse, TinyPNGError
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen, HTTPError


TINYPNG_SHRINK_URL = "https://api.tinypng.com/shrink"
TINYPNG_SUCCESS = 201
TINYPNG_SLEEP_SEC = 1

class StopProcessing(Exception): pass
class RetryProcessing(Exception): pass

def tinypng_compress(image, apikey):
    def process_response(response):
        json_res = json.loads(response.read())
        if response.code == TINYPNG_SUCCESS:
            json_res['location'] = response.headers.getheader("Location")
            try:
                json_res['output'] = urlopen(json_res['location']).read()
            except:
                json_res['output'] = None
        return (response.code, json_res)

    if not apikey:
        raise ValueError("TinyPNG API KEY is not set")

    request = Request(TINYPNG_SHRINK_URL, image)
    auth = b64encode(bytes("api:" + apikey)).decode("ascii")
    request.add_header("Authorization", "Basic %s" % auth)
    try:
        response = urlopen(request)
        (code, response_dict) = process_response(response)
    except HTTPError as e:
        (code, response_dict) = process_response(e)
    return TinyPNGResponse(code, **response_dict)


basecallback = lambda x: x
def tinypng_process_directory(source, dest, apikey, callback=basecallback):
    def process_file(input_file):
        bytes_ = open(input_file, 'rb').read()
        compressed = tinypng_compress(bytes_, apikey)
        callback(compressed)

        if compressed.success and compressed.output:
            target_dir, filename = target_path(source, dest, input_file)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            open(os.path.join(target_dir, filename), 'wb+').write(compressed.output)
        else:
            if compressed.errno in (TinyPNGError.Unauthorized, TinyPNGError.TooManyRequests):
                raise StopProcessing()
            if compressed.errno == TinyPNGError.InternalServerError:
                raise RetryProcessing()

        return compressed

    attemps = defaultdict(lambda: 0)
    input_files = files_with_exts(source, suffix='.png')
    input_file = next(input_files, None)
    while input_file:
        try:
            process_file(input_file)
            input_file = next(input_files, None)
        except StopProcessing:
            break
        except RetryProcessing:
            time.sleep(TINYPNG_SLEEP_SEC)
            if attemps[input_file] < 9:
                attemps[input_file] += 1
            else:
                input_file = next(input_files, None)


def target_path(source, dest, input_file):
    dirname = os.path.dirname(input_file).replace(source, '')[1:]
    filename = os.path.basename(input_file)
    target_dir = os.path.join(dest, dirname)
    target_file = os.path.join(target_dir, filename)
    return (target_dir, target_file)


def files_with_exts(root='.', suffix=''):
    return (os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(root)
            for filename in filenames 
            if filename.endswith(suffix))

def main():
    tinypng_process_directory('input', 'output')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('key', help='TinyPNG API Key')
    parser.add_argument('origin', help='Input directory with PNG files')
    parser.add_argument('target', help='Output directory')

    args = parser.parse_args()
