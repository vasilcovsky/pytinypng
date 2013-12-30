import pytest
from .helper import *
from .. import pytinypng


def _callback(compressed):
    _callback.total += 1


def test_tinypng_process():
    _callback.total = 0

    (fake_fs, fake_os, fake_open) = init_filesystem()

    pytinypng.os = fake_os
    pytinypng.open = fake_open
    
    with success_result():
        pytinypng.tinypng_process_directory('/input', '/output', '12345', _callback)
        assert fake_os.path.exists('/output/subdir/a/bullet.png') == True
        assert _callback.total == 2


def test_tinypng_process_stop():
    def fake_compress(*args):
        return pytinypng.TinyPNGResponse(500, error='TooManyRequests', message='...')

    _callback.total = 0

    pytinypng.tinypng_compress = fake_compress

    (fake_fs, fake_os, fake_open) = init_filesystem()

    pytinypng.os = fake_os
    pytinypng.open = fake_open
    pytinypng.tinypng_process_directory('/input', '/output', '12345', _callback)
    assert _callback.total == 1

