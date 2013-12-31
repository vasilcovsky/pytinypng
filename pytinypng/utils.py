import os


class Enum:
    @classmethod
    def from_value(cls, value):
        if value in cls.__dict__:
            return cls.__dict__[value]
        raise AttributeError("Not found value %s" % value)


def files_with_exts(root='.', suffix=''):
    return (os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(root)
            for filename in filenames
            if filename.endswith(suffix))


def target_path(source, dest, input_file):
    dirname = os.path.dirname(input_file).replace(source, '')[1:]
    filename = os.path.basename(input_file)
    target_dir = os.path.join(dest, dirname)
    target_file = os.path.join(target_dir, filename)
    return (target_dir, filename)