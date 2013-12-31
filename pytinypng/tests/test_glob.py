import pytinypng.pytinypng as pytinypng
from pytinypng import utils
from pytinypng.tests.helper import *

def test_files_with_exts():
    fake_fs, fake_os, fake_open = init_filesystem()
    utils.os = fake_os
    pytinypng.open = fake_open
    files = utils.files_with_exts('input', '.png')
    assert files