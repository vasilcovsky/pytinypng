from collections import defaultdict
from utils import Enum


class TinyPNGError(Enum):
    """List of error codes returned by TinyPNG API"""
    Unauthorized = 1
    InputMissing = 2
    BadSignature = 3
    DecodeError = 4
    TooManyRequests = 5
    InternalServerError = 6


FATAL_ERRORS = (TinyPNGError.Unauthorized, TinyPNGError.TooManyRequests)


class TinyPNGResponse:
    """Immutable class to represent TinyPNG response"""

    SUCCESS_CODE = 201

    def __init__(self, status, **kwargs):
        self._status = status
        self._response = kwargs
        self._properties = defaultdict(lambda: None)
        self._properties.update(kwargs)

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
        err = self._properties['error']
        if err:
            return TinyPNGError.from_value(err)
        return None

    @property
    def errmsg(self):
        return self._properties['message']

    @property
    def input_size(self):
        input = self._properties['input']
        if input and 'size' in input:
            return input['size']
        return None

    @property
    def output_size(self):
        output = self._properties['output']
        if output and 'size' in output:
            return output['size']
        return None

    @property
    def output_ratio(self):
        output = self._properties['output']
        if output and 'ratio' in output:
            return output['ratio']
        return None

    @property
    def compressed_image_url(self):
        return self._properties['location']

    @property
    def bytes(self):
        return self._properties['bytes']
