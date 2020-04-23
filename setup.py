from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ordinary_portal',
    version='0.3a',
    url='https://github.com/lukestanley/ordinary-portal',
    license='GPL',
    author='Luke Stanley',
    install_requires=required,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ordinary_portal=ordinary_portal.portal_uploader:main',
        ],
    },
)
