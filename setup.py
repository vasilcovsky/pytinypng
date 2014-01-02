from setuptools import setup
from pytinypng import __version__

print __version__

setup(
    name='pytinypng.py',
    version=__version__,
    description='Batch compression for PNG images',
    long_description='pytinypng.py is a batch image compression tool for optimizing '
                     'thousands of images in png format.'
                     'Under the hook it uses tinypng.com API to shrink png files.',
    keywords='tinyping compression png optimization',
    author='Igor Vasilcovsky',
    author_email='vasilcovsky@gmail.com',
    url='http://github.com/vasilcovsky/pytinypng.py',
    license='BSD License',
    packages=['pytinypng'],
    install_requires=[],
    scripts=['pytinypng/bin/pytinypng.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Archiving :: Compression'
    ]
)