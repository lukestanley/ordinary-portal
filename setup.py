from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ordinary_portal',
    version='0.1a',
    url='https://github.com/lukestanley/ordinary-portal',
    license='GPL',
    author='Luke Stanley',
    author_email='',
    description='',
    install_requires=required,
)
