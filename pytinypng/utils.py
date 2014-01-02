import os


class Enum:
    """Used to access integer constants by string code.

    >>> class Color(Enum):
    ...     RED = 1
    ...     YELLOW = 2
    ...     GREEN = 3
    ...
    >>> Color.from_value("RED")
    1
    """
    @classmethod
    def from_value(cls, value):
        if value in cls.__dict__:
            return cls.__dict__[value]
        raise AttributeError("Not found value %s" % value)


def write_binary(filename, data):
    """Create path to filename and saves binary data"""
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(filename, 'wb') as f:
        f.write(data)


def read_binary(filename):
    """Read binary data from filename"""
    with open(filename, 'rb') as f:
        return f.read()


def files_with_exts(root='.', suffix=''):
    """Returns generator that contains filenames
       from root directory and ends with suffix
    """
    return (os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(root)
            for filename in filenames
            if filename.endswith(suffix))


def target_path(source_dir, target_dir, input_file):
    rel_target_dir = os.path.dirname(input_file).replace(source_dir, '')[1:]
    basename = os.path.basename(input_file)
    dirname = os.path.join(target_dir, rel_target_dir)
    realpath = os.path.join(dirname, basename)
    return realpath


def size_fmt(num):
    """Generate a string representation for the given byte count.
    >>> size_fmt(12345)
    '12.1KB'
    """
    for x in ['b', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%.1f%s" % (num, x)
        num /= 1024.0
    return "%.1f%s" % (num, 'TB')


def find_apikey():
    """Finds TinyPNG API key

    Search for api key in following order:
     - environment variable TINYPNG_APIKEY
     - environment variable TINYPNG_API_KEY
     - file in local directory tinypng.key
     - file in home directory ~/.tinypng.key

    If key not found returns None
    """
    env_keys = ['TINYPNG_APIKEY', 'TINYPNG_API_KEY']
    paths = []
    paths.append(os.path.join(os.path.abspath("."), "tinypng.key"))  # local directory
    paths.append(os.path.expanduser("~/.tinypng.key"))  # home directory

    for env_key in env_keys:
        if os.environ.get(env_key):
            return os.environ.get(env_key)

    for path in paths:
        if os.path.exists(path):
            return open(path, 'rt').read()

    return None


def _decorated_msg(code):
    return lambda msg: code + msg + '\033[0m'


bold = _decorated_msg('\033[1m')
green = _decorated_msg('\033[92m')
red = _decorated_msg('\033[91m')
yellow = _decorated_msg('\033[93m')
