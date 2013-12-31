from utils import Enum


class TinyPNGError(Enum):
    Unauthorized = 1
    InputMissing = 2
    BadSignature = 3
    DecodeError = 4
    TooManyRequests = 5
    InternalServerError = 6


class TinyPNGResponse:

    SUCCESS_CODE = 201

    def __init__(self, status, **kwargs):
        self._status = status
        self._response = kwargs

    @property
    def status(self):
        return self._status

    @property
    def success(self):
        return self.status == self.SUCCESS_CODE

    @property
    def failure(self):
        return not self.success

    @property
    def errno(self):
        err = self._from_response('error')
        if err:
            return TinyPNGError.from_value(err)
        return None

    @property
    def errmsg(self):
        return self._from_response('message')

    @property
    def input_size(self):
        input_ = self._from_response('input')
        if input_:
           return input_['size']

    @property
    def output_size(self):
        output = self._from_response('output')
        if output:
            return output['size']

    @property
    def output_ratio(self):
        output = self._from_response('output')
        if output:
            return output['ratio']

    @property
    def compressed_image_url(self):
        return self._from_response('location')

    @property
    def bytes(self):
        return self._from_response('bytes')

    @property
    def filename(self):
        return self._from_response('filename') or ''

    def _from_response(self, key, default=None):
        if key in self._response:
            return self._response[key]
        return default