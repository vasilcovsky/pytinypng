from pytinypng.utils import Enum


class TinyPNGError(Enum):
    Unauthorized = 1
    InputMissing = 2
    BadSignature = 3
    DecodeError = 4
    TooManyRequests = 5
    InternalServerError = 6


class TinyPNGResponse:
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
        if err:
            return TinyPNGError.fromValue(err)
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
