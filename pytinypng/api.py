import json
from base64 import b64encode
from domain import TinyPNGResponse
from urllib2 import Request, urlopen, HTTPError


TINYPNG_SHRINK_URL = "https://api.tinypng.com/shrink"


def shrink(image, apikey):
    """To shrink a PNG image, post the data to the API service.
    The response is a JSON message.
    The initial request must be authorized with HTTP Basic authorization.

    @param image: PNG image bytes sequence
    @param apikey: TinyPNG API key
    @param filename: filename of input file
    """

    def _handle_response(response):
        body = json.loads(response.read())
        if response.code == TinyPNGResponse.SUCCESS_CODE:
            body['location'] = response.headers.getheader("Location")
            try:
                body['bytes'] = urlopen(body['location']).read()
            except:
                body['bytes'] = None
        return response.code, body

    auth = b64encode(bytes("api:" + apikey)).decode("ascii")

    request = Request(TINYPNG_SHRINK_URL, image)
    request.add_header("Authorization", "Basic %s" % auth)

    try:
        response = urlopen(request)
        (code, response_dict) = _handle_response(response)
    except HTTPError as e:
        (code, response_dict) = _handle_response(e)

    return TinyPNGResponse(code, **response_dict)
