import json
import httpretty
import fake_filesystem
from contextlib import contextmanager
from pytinypng.api import TINYPNG_SHRINK_URL
from pytinypng.handlers import BaseHandler


@contextmanager
def success_result():
    expected_body = {
        "input": {"size": 100},
        "output": {"size": 50, "ratio": 2}
    }

    compressed_img_location = "https://api.tinypng.com/output/2xnsp7jn34e5.png"

    httpretty.enable()
    httpretty.register_uri(httpretty.POST, TINYPNG_SHRINK_URL,
                           body=json.dumps(expected_body),
                           content_type="application/json",
                           location=compressed_img_location,
                           status=201)
    httpretty.register_uri(httpretty.GET, compressed_img_location,
                           content_type="image/png", status=200,
                           body='<compressed image bytes>')
    yield
    httpretty.disable()


@contextmanager
def failure(code=500, error="TooManyRequests"):
    expected_body = dict(error=error, message="...")

    httpretty.enable()
    httpretty.register_uri(httpretty.POST, TINYPNG_SHRINK_URL,
                 body=json.dumps(expected_body),
                 content_type="application/json",
                 status=code)
    yield
    httpretty.disable()


def init_filesystem():
    fake_fs  = fake_filesystem.FakeFilesystem()
    fake_os = fake_filesystem.FakeOsModule(fake_fs)
    fake_open = fake_filesystem.FakeFileOpen(fake_fs)
    files = ['/input/subdir/a/bullet.png', '/input/subdir/b/photo.jpg',
             '/input/subdir/a/style/header.png']

    for filename in files:
        fake_fs.CreateFile(filename)

    return (fake_fs, fake_os, fake_open)


class TestHandler(BaseHandler):
    def __init__(self):
        self.retry_no = 0
        self.skip_no = 0
        self.finish_no = 0
        self.post_no = 0
        self.pre_no = 0
        self.start_no = 0

    def on_retry(self, input_file):
        self.retry_no += 1

    def on_skip(self, input_file):
        self.skip_no += 1

    def on_finish(self):
        self.finish_no += 1

    def on_pre_item(self, input_file):
        self.pre_no += 1

    def on_post_item(self, image, input_file):
        self.post_no += 1

    def on_start(self):
        self.start_no += 1
