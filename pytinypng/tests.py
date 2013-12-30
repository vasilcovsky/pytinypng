import unittest
import json
import pytinypng
from pytinypng import tinypng_process_directory
import httpretty
from httpretty import register_uri
import fake_filesystem


class TinyPNGTest(unittest.TestCase):

    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()

    def test_tinypng_compress(self):
        expected = {
            "input.size": 100,
            "output.size": 50,
            "output.ratio": 2
        }

        register_uri(httpretty.POST, pytinypng.TINYURL_SHRINK_URL,
                     body=json.dumps(expected),
                     content_type="application/json",
                     location="http://example.org/compressed.png",
                     status=201)

        compressed = pytinypng.tinypng_compress('')

        self.assertTrue(compressed.success)
        self.assertFalse(compressed.failure)
        self.assertEqual(compressed.compressed_image_url, "http://example.org/compressed.png")
        items = [compressed.input_size, compressed.output_size, compressed.output_ratio]
        self.assertTrue(all(items))

        errors = [compressed.errno, compressed.errmsg]
        self.assertFalse(any(errors))

    def test_tinypng_download(self):
        compressed_img_url = 'http://example.org/compressed.png'

        register_uri(httpretty.GET, compressed_img_url, body='Image')

        content = pytinypng.tinypng_download(compressed_img_url)
        self.assertEquals(content, 'Image')

    def test_tinypng_process(self):
        filesystem = fake_filesystem.FakeFilesystem()
        os_module = fake_filesystem.FakeOsModule(filesystem)
        files = ['/input/subdir/a/bullet.png', '/input/subdir/b/photo.jpg',
                 '/input/subdir/a/style/header.png']

        os_ = pytinypng.os
        pytinypng.os = os_module
        pytinypng.open = fake_filesystem.FakeFileOpen(filesystem)

        for filename in files:
            filesystem.CreateFile(filename)
    
        tinypng_process_directory('/input', '/output')

        self.assertTrue(os_module.path.exists('/output/subdir/a/bullet.png'))
        self.assertTrue(os_module.path.exists('/output/subdir/a/style/header.png'))
        self.assertFalse(os_module.path.exists('/output/subdir/b/photo.jpg'))
        

if __name__ == '__main__':
    unittest.main()
