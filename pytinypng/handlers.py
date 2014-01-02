from __future__ import print_function
from utils import size_fmt, bold, yellow, red, green

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


class ScreenHandler(BaseHandler):

    def __init__(self):
        self._optimized = 0
        self._skipped = 0
        self._failed = 0
        self._input_bytes = 0
        self._output_bytes = 0

    def on_skip(self, input_file):
        self._skipped += 1
        filename = self.format_filename(input_file)
        print("%s %18s %30s" % (filename, yellow("SKIP"), "-"))

    def on_post_item(self, response, input_file):
        filename = self.format_filename(input_file)
        if response.success:
            self._optimized += 1
            self._input_bytes += response.input_size
            self._output_bytes += response.output_size
            print("%s %16s %37s" % (filename, green("OK"), response.output_ratio))
        else:
            self._failed += 1
            print("%s %18s %30s" % (filename, red("FAIL"), "-"))

    def on_start(self):
        print("\n%s %45s %40s\n" % (bold("FILE"), bold("STATUS"), bold("RATIO")))

    def on_finish(self):
        optimized = "%(optimized)s (%(input)s -> %(output)s)"
        optimized = optimized % dict(optimized=self._optimized,
                                     input=size_fmt(self._input_bytes),
                                     output=size_fmt(self._output_bytes))
        print()
        print(bold("Optimized: ") + optimized, end="\t")
        print(bold("Skipped: ") + str(self._skipped), end="\t")
        print(bold("Failed: ") + str(self._failed), end="\t")
        print("\n\n")

    def format_filename(self, filename):
        filename_ = filename[-27:].ljust(27, ' ')
        if filename > 30:
            filename_ = '...' + filename_

        return filename_