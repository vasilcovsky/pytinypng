import os


class Enum:
    @classmethod
    def from_value(cls, value):
        if value in cls.__dict__:
            return cls.__dict__[value]
        raise AttributeError("Not found value %s" % value)


def write_binary(filename, data):
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(filename, 'wb') as f:
        f.write(data)


def read_binary(filename):
    with open(filename, 'rb') as f:
        return f.read()

def files_with_exts(root='.', suffix=''):
    return (os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(root)
            for filename in filenames
            if filename.endswith(suffix))


def target_path(source_dir, target_dir, input_file):
    rel_target_dir = os.path.dirname(input_file).replace(source_dir, '')[1:]
    basename = os.path.basename(input_file)
    dirname = os.path.join(target_dir, rel_target_dir)
    realpath = os.path.join(dirname, basename)
    return (dirname, basename, realpath)


def size_fmt(num):
    for x in ['b', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%.1f%s" % (num, x)
        num /= 1024.0
    return "%.1f%s" % (num, 'TB')


def _decorated_msg(code):
    return lambda msg: code + msg + '\033[0m'


bold = _decorated_msg('\033[1m')
green = _decorated_msg('\033[92m')
red = _decorated_msg('\033[91m')
yellow = _decorated_msg('\033[93m')
