import pytest
from .. import pytinypng
from .helper import *

def test_files_with_exts():
    fake_fs, fake_os, fake_open = init_filesystem()
    pytinypng.os = fake_os
    pytinypng.open = fake_open
    files = pytinypng.files_with_exts('input', '.png')
    assert files