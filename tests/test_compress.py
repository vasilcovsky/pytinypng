import pytest
from pytinypng.api import shrink
from pytinypng.domain import TinyPNGError
from tests.helper import success_result, failure

def test_tinypng_compress():
    with success_result():
        compressed = shrink('<image bytes>', apikey='12345')
        assert compressed.success == True
        assert compressed.failure == False
        assert compressed.input_size == 100
        assert compressed.output_size == 50
        assert compressed.output_ratio == 2
        assert compressed.bytes == '<compressed image bytes>'
        assert compressed.errno == None


def test_tinypng_compress_error():
    with failure():
        compressed = shrink('<image bytes>', apikey='12345')
        assert compressed.failure == True
        assert compressed.errno == TinyPNGError.TooManyRequests
        assert compressed.bytes == None
