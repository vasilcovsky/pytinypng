import json
from base64 import b64encode
from domain import TinyPNGResponse

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen, HTTPError


TINYPNG_SHRINK_URL = "https://api.tinypng.com/shrink"

def shrink(image, apikey, filename=None):
    def _handle_response(response):
        json_res = json.loads(response.read())
        if response.code == TinyPNGResponse.SUCCESS_CODE:
            json_res['location'] = response.headers.getheader("Location")
            try:
                json_res['bytes'] = urlopen(json_res['location']).read()
            except:
                json_res['bytes'] = None
        json_res['filename'] = filename
        return (response.code, json_res)

    if not apikey:
        raise ValueError("TinyPNG API KEY is not set")

    request = Request(TINYPNG_SHRINK_URL, image)
    auth = b64encode(bytes("api:" + apikey)).decode("ascii")
    request.add_header("Authorization", "Basic %s" % auth)
    try:
        response = urlopen(request)
        (code, response_dict) = _handle_response(response)
    except HTTPError as e:
        (code, response_dict) = _handle_response(e)
    return TinyPNGResponse(code, **response_dict)