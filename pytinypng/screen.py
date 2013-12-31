def bold(msg):
    return '\033[1m' + msg + '\033[0m'


def green(msg):
    return '\033[92m' + msg + '\033[0m'


def red(msg):
    return '\033[91m' + msg + '\033[0m'


def yellow(msg):
    return '\033[93m' + msg + '\033[0m'

def table_header():
    print("\n%s %45s %40s\n" % (bold("FILE"), bold("STATUS"), bold("RATIO")))


def item_row(image, filename):
    """
    @type image: TinyPNGResponse
    """
    filename = filename[-30:].ljust(30, ' ')

    if image.success:
        print("%s %16s %37s" % (filename, green("OK"), image.output_ratio))
    else:
        print("%s %18s %30s" % (filename, red("FAIL"), "-"))


def skip_item(filename):
    filename = filename[-30:].ljust(30, ' ')
    print("%s %18s %30s" % (filename, yellow("SKIP"), "-"))


if __name__ == '__main__':
    table_header()
    from collections import namedtuple
    result = namedtuple("Result", "filename, success, output_ratio")
    import random
    import string
    for x in range(10):
        filename = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(4, 30)))
        r = result(filename, random.choice([True, False]), random.randrange(1, 10))
        item_row(r)
    print "\n"