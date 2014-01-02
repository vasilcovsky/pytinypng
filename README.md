#  Batch compression for PNG images

```pytinypng``` is a batch image compression tool for optimizing thousands of images in png format. Under the hood it uses [tinypng.com](http://tinypng.com) API to shrink png files.

![Console screenshot](https://raw.github.com/vasilcovsky/pytinypng/master/content/console1.png)

**Features**
 * Optimized files are saving on disk keeping original directory structure
 * Skip already optimized files.

## Installation
 1. Obtain TinyPNG API key on [Developer API page](https://api.tinypng.com/developers)
 2. ...

## Usage
```pytinypng input-directory output-directory --apikey <API_KEY>```
