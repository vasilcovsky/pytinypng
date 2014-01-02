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

    def __init__(self, response_code, **kwargs):
        self._response_code = response_code
        self._response = kwargs
        self._properties = defaultdict(lambda: None)
        self._properties.update(kwargs)

    @property
    def response_code(self):
        return self._response_code

    @property
    def success(self):
        return self.response_code == self.SUCCESS_CODE

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
        input_ = self._properties['input']
        if input_:
            return input_.get('size')
        return None

    @property
    def output_size(self):
        output = self._properties['output']
        if output:
            return output.get('size')
        return None

    @property
    def output_ratio(self):
        output = self._properties['output']
        if output:
            return output.get('ratio')
        return None

    @property
    def compressed_image_url(self):
        return self._properties['location']

    @property
    def bytes(self):
        return self._properties['bytes']
