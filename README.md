#  Batch compression for PNG images

**pytinypng** is a batch image compression tool for optimizing thousands of images in png format. Under the hood it uses [tinypng.com](http://tinypng.com) API to shrink png files.

![Console screenshot](https://raw.github.com/vasilcovsky/pytinypng/master/content/console1.png)

**Features**
 * Optimized files are saving on disk keeping original directory structure
 * Skip already optimized files.

## Installation
Get Python 2.7 at [http://www.python.org](http://www.python.org). If you’re running Linux or Mac OS X, you probably
already have it installed.

If you are on Mac OS X or Linux, chances are that one of the following two commands will work for you:

```$ sudo easy_install pytinypng```

or even better:

```$ sudo pip install pytinypng```

and then obtain TinyPNG API key from
[Developer API page](https://api.tinypng.com/).

## Usage
Run in terminal:

```pytinypng /path/to/directory/with/png-images /path/to/output-directory --apikey <API_KEY>```

You can hide api key from command line in:
  * environment variable *TINYPNG_APIKEY* or *TINYPNG_API_KEY*
  * inside file located in working directory under name *tinypng.key*
  * or keep in your home directory as *~/.tinypng.key*
