from setuptools import setup, find_packages
import os


def readme_contents(default=None):
    readme = default

    if not os.path.exists(readme_file):
        return
    with open(readme_file, 'r') as ff:
        readme = ff.read()

    return readme


readme_file = 'README.md'
description = 'A library for interacting with the App.net API.'
requires = ['requests',
            'python-dateutil']

setup(
    name='appdotnet',
    version='0.1.0',
    description=description,
    long_description=readme_contents(default=description),
    author='Brian Cline',
    author_email='bc@brian.fm',
    url='https://github.com/briancline/appdotnet',
    license='The BSD License',

    install_requires=requires,
    packages=find_packages(),

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',
    ]
)
