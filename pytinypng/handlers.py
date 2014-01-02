from __future__ import print_function


class BaseHandler:
    def __init__(self):
        pass

    def on_start(self):
        pass

    def on_start(self):
        pass

    def on_retry(self, input_file):
        pass

    def on_skip(self, input_file):
        pass

    def on_pre_item(self, input_file):
        pass

    def on_post_item(self, image, input_file):
        pass

    def on_finish(self):
        pass


def _decorated_msg(code):
    return lambda msg: code + msg + '\033[0m'


bold = _decorated_msg('\033[1m')
green = _decorated_msg('\033[92m')
red = _decorated_msg('\033[91m')
yellow = _decorated_msg('\033[93m')


class ScreenHandler(BaseHandler):
    def format_filename(self, filename):
        return filename[-30:].ljust(30, ' ')

    def on_skip(self, input_file):
        self._skipped += 1
        filename = self.format_filename(input_file)
        print("%s %18s %30s" % (filename, yellow("SKIP"), "-"))

    def on_post_item(self, response, input_file):
        filename = self.format_filename(input_file)
        if response.success:
            self._optimized += 1
            print("%s %16s %37s" % (filename, green("OK"), response.output_ratio))
        else:
            print("%s %18s %30s" % (filename, red("FAIL"), "-"))

    def on_start(self):
        print("\n%s %45s %40s\n" % (bold("FILE"), bold("STATUS"), bold("RATIO")))

    def on_finish(self):
        print()
        print(bold("Optimized: ") + str(self._optimized), end="\t")
        print(bold("Skipped: ") + str(self._skipped), end="\t")
        print(bold("Failed: ") + str(self._failed), end="\t")
        print("\n\n")

    def __init__(self):
        self._optimized = 0
        self._skipped = 0
        self._failed = 0