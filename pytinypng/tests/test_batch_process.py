from .. import pytinypng
from pytinypng import utils
from pytinypng.domain import TinyPNGResponse
from pytinypng.tests.helper import success_result, init_filesystem, TestHandler

def test_tinypng_process():
    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    utils.open = fake_open
    pytinypng.os = fake_os

    with success_result():
        handler = TestHandler()
        pytinypng.process_directory('/input', '/output', '12345', handler)
        assert fake_os.path.exists('/output/subdir/a/bullet.png')
        assert handler.post_no == 2


def test_tinypng_process_stop():
    def fake_compress(*args):
        return TinyPNGResponse(500, error='TooManyRequests', message='...')

    shrink = fake_compress

    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    utils.open = fake_open
    pytinypng.os = fake_os

    handler = TestHandler()

    pytinypng.process_directory('/input', '/output', '12345', handler)
    assert handler.post_no == 1


def test_tinypng_process_retry():
    def fake_compress(*args):
        return TinyPNGResponse(500, error='InternalServerError', message='...')

    pytinypng.TINYPNG_SLEEP_SEC = 0
    shrink = fake_compress

    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    utils.open = fake_open
    pytinypng.os = fake_os

    handler = TestHandler()

    pytinypng.process_directory('/input', '/output', '12345', handler)
    assert handler.post_no == 1


def test_tinypng_process_allow_overwrite():
    (fake_fs, fake_os, fake_open) = init_filesystem()

    utils.os = fake_os
    utils.open = fake_open
    pytinypng.os = fake_os
    pytinypng.open = fake_open

    fake_fs.CreateFile("/output/subdir/a/bullet.png")

    with success_result():
        handler = TestHandler()
        pytinypng.process_directory('/input', '/output', '12345', handler)
        assert handler.post_no == 1
