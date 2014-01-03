from __future__ import print_function
from utils import size_fmt, bold, yellow, red, green
from os import path

class BaseHandler:
    def __init__(self):
        pass

    def on_start(self):
        pass

    def on_stop(self, errmsg):
        pass

    def on_retry(self, input_file):
        pass

    def on_skip(self, input_file, **kwargs):
        pass

    def on_pre_item(self, input_file, **kwargs):
        pass

    def on_post_item(self, image, **kwargs):
        pass

    def on_finish(self, **kwargs):
        pass


class ScreenHandler(BaseHandler):

    def __init__(self):
        self._optimized = 0
        self._skipped = 0
        self._failed = 0
        self._input_bytes = 0
        self._output_bytes = 0

    def on_skip(self, input_file, **kwargs):
        source = kwargs.get('source', '')

        self._skipped += 1

        filename = self.format_filename(input_file.replace(source, ''))
        print("%s %18s %30s" % (filename, yellow("SKIP"), "-"))

    def on_post_item(self, response, **kwargs):
        input_file = kwargs.get('input_file', '')
        source = kwargs.get('source', '')

        filename = self.format_filename(input_file.replace(source, ''))
        if response.success:
            self._optimized += 1
            self._input_bytes += response.input_size
            self._output_bytes += response.output_size
            print("%s %16s %37s" % (filename, green("OK"),
                                    response.output_ratio))
        else:
            self._failed += 1
            print("%s %18s %30s" % (filename, red("FAIL"), "-"))

    def on_start(self):
        print("\n%s %45s %40s\n" % (bold("FILE"), bold("STATUS"),
                                    bold("RATIO")))

    def on_stop(self, errmsg):
        print("Error: " + errmsg)
        print()

    def on_finish(self, **kwargs):
        output_dir = kwargs.get('output_dir', '')
        optimized = "%(optimized)s (%(input)s -> %(output)s)"
        optimized = optimized % dict(optimized=self._optimized,
                                     input=size_fmt(self._input_bytes),
                                     output=size_fmt(self._output_bytes))
        print()
        print(bold("Optimized: ") + optimized, end="\t")
        print(bold("Skipped: ") + str(self._skipped), end="\t")
        print(bold("Failed: ") + str(self._failed), end="\t")
        print("\n")
        print("Optimized files were saved to:\n%s" % output_dir)
        print("\n\n")

    def format_filename(self, filename):
        if filename.startswith(path.sep):
            filename = filename[1:]

        filename_ = filename[-30:]
        if len(filename) > 30:
            filename_ = '...' + filename_[3:]
        filename_ = filename_.ljust(30, ' ')
        return filename_
