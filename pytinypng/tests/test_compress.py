import json
import pytest
from .helper import *
from ..pytinypng import tinypng_compress, TinyPNGError


def test_tinypng_compress():
    with success_result():
        compressed = tinypng_compress('<image bytes>', apikey='12345')
        assert compressed.success == True
        assert compressed.failure == False
        assert compressed.input_size == 100
        assert compressed.output == '<compressed image bytes>'
        assert compressed.errno == None


def test_tinypng_compress_empty_key():
    """tinypng_compress should raise ValueError if apikey is empty""" 
    with pytest.raises(ValueError):
        compressed = tinypng_compress('<image bytes>', '')


def test_tinypng_compress_error():
    with failure():
        compressed = tinypng_compress('<image bytes>', apikey='12345')
        assert compressed.failure == True
        assert compressed.errno == TinyPNGError.TooManyRequests
        assert compressed.output == None
