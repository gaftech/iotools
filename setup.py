# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = __import__('iotools').__version__

setup(
    name = "iotools",
    version = version,
    author = 'Gabriel Fournier',
    author_email = 'gabriel@gaftech.fr',
    url = 'http://redmine.sticfm.fr/iotools',
    packages = find_packages(),
    entry_points = """
    [console_scripts]
    modbus = iotools.modbus.cli:main
    """
)
