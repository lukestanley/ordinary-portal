from setuptools import find_packages, setup
from os.path import abspath, dirname, join

with open("requirements.txt") as f:
    required = f.read().splitlines()

this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.rst"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="ordinary_portal",
    version="0.4a",
    url="https://github.com/lukestanley/ordinary-portal",
    description="Send small files from one machine to another securely,"
    " without messing with ports, or waiting for encryption modules to build.",
    long_description=long_description,
    license="GPL",
    author="Luke Stanley",
    install_requires=required,
    packages=find_packages(),
    entry_points={
        "console_scripts": ["ordinary_portal=ordinary_portal.__main__:main",],
    },
)
