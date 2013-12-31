from .. import pytinypng
from pytinypng import utils
from pytinypng.domain import TinyPNGResponse
from pytinypng.tests.helper import success_result, init_filesystem


def _callback(compressed, filename=None):
    _callback.total += 1


def test_tinypng_process():
    _callback.total = 0

    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    pytinypng.os = fake_os
    pytinypng.open = fake_open

    with success_result():
        pytinypng.process_directory('/input', '/output', '12345', item_callback=_callback)
        assert fake_os.path.exists('/output/subdir/a/bullet.png') == True
        assert _callback.total == 2


def test_tinypng_process_stop():
    def fake_compress(*args):
        return TinyPNGResponse(500, error='TooManyRequests', message='...')

    _callback.total = 0

    shrink = fake_compress

    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    pytinypng.os = fake_os

    pytinypng.open = fake_open
    pytinypng.process_directory('/input', '/output', '12345', item_callback=_callback)
    assert _callback.total == 1


def test_tinypng_process_retry():
    def fake_compress(*args):
        return TinyPNGResponse(500, error='InternalServerError', message='...')

    _callback.total = 0

    pytinypng.TINYPNG_SLEEP_SEC = 0
    shrink = fake_compress

    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    pytinypng.os = fake_os
    pytinypng.open = fake_open
    pytinypng.process_directory('/input', '/output', '12345', item_callback=_callback)
    assert _callback.total == 1


def test_tinypng_process_allow_overwrite():
    _callback.total = 0

    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    pytinypng.os = fake_os
    pytinypng.open = fake_open

    fake_fs.CreateFile("/output/subdir/a/bullet.png")

    with success_result():
        pytinypng.process_directory('/input', '/output', '12345', item_callback=_callback)
        assert _callback.total == 1