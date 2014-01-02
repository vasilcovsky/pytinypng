from setuptools import setup, find_packages
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
    url='https://github.com/vasilcovsky/pytinypng',
    license='BSD License',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'pytinypng = pytinypng.pytinypng:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Archiving :: Compression'
    ]
)