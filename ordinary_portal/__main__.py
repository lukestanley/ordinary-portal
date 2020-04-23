#!/usr/bin/env python
"""ordinary_portal

Send small files like SSH keys from one system to another with Python dependencies.
An experiment in readable everyday cryptography, inspired by magic-wormhole.

Usage:
  ordinary_portal send
  ordinary_portal send <filename>...
  ordinary_portal download
  ordinary_portal download <pass_phrase>...
  ordinary_portal (-h | --help)

Options:
  -h --help     Show this screen.

"""


from docopt import docopt

from ordinary_portal.send import send
from ordinary_portal.download import download
from ordinary_portal.config import is_testing


def main():
    arguments = docopt(__doc__)
    if is_testing:
        print('Arguments received:', arguments)
    if arguments['send']:
        filename = arguments.get('<filename>', [None])[0]
        send(filename=filename)
    if arguments['download']:
        pass_phrase_list = arguments.get('<pass_phrase>', None)
        if pass_phrase_list:
            pass_string = ' '.join(pass_phrase_list)
        download(pass_string)
