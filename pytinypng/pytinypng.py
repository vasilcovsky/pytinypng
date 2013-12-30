import os
import glob
import json
import argparse
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen, HTTPError

from base64 import b64encode

TINYPNG_SHRINK_URL = "https://api.tinypng.com/shrink"
TINYPNG_SUCCESS = 201

class TinyPNGError:
    Unauthorized = 1
    InputMissing = 2
    BadSignature = 3
    DecodeError = 4
    TooManyRequests = 5
    InternalServerError = 6

class TinyPNGResponse:
    errors = {
        "Unauthorized": TinyPNGError.Unauthorized,
        "InputMissing": TinyPNGError.InputMissing,
        "BadSignature": TinyPNGError.BadSignature,
        "DecodeError": TinyPNGError.DecodeError,
        "TooManyRequests": TinyPNGError.TooManyRequests,
        "InternalServerError": TinyPNGError.InternalServerError
    }

    def __init__(self, status, **kwargs):
        self._status = status
        self._response = kwargs

    @property
    def status(self):
        return self._status

    @property
    def success(self):
        return self.status == TINYPNG_SUCCESS

    @property
    def failure(self):
        return not self.success

    @property
    def errno(self):
        err = self._from_response('error')
        if err in self.errors:
            return self.errors[err]
        return None

    @property
    def errmsg(self):
        return self._from_response('message')

    @property
    def input_size(self):
        return self._from_response('input.size')

    @property
    def output_size(self):
        return self._from_response('output.size')

    @property
    def output_ratio(self):
        return self._from_response('output.ratio')

    @property
    def compressed_image_url(self):
        return self._from_response('location')

    @property
    def output(self):
        return self._from_response('output')

    def _from_response(self, key, default=None):
        if key in self._response:
            return self._response[key]
        return default

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
            dirname = os.path.dirname(input_file).replace(source, '')[1:]
            filename = os.path.basename(input_file)
            target_dir = os.path.join(dest, dirname)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            open(os.path.join(target_dir, filename), 'wb+').write(compressed.output)
        else:
            if compressed.errno in (TinyPNGError.Unauthorized, TinyPNGError.TooManyRequests):
                raise StopProcessing()
            if compressed.errno == TinyPNGError.InternalServerError:
                raise RetryProcessing()

        return compressed

    input_files = files_with_exts(source, suffix='.png')

    while input_files:
        input_file = input_files.pop()
        try:
            process_file(input_file)
        except StopProcessing:
            break
        except RetryProcessing:
            pass



def files_with_exts(root='.', suffix=''):
    return [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(root)
            for filename in filenames 
            if filename.endswith(suffix)]

def main():
    tinypng_process_directory('input', 'output')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('key', help='TinyPNG API Key')
    parser.add_argument('origin', help='Input directory with PNG files')
    parser.add_argument('target', help='Output directory')

    args = parser.parse_args()
