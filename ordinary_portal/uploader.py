from uuid import uuid4

from websocket import WebSocketApp as WebSocketClient
from ordinary_portal.utils import (
    encrypt_binary_payload_with_session_key_and_public_key,
    make_key_of_set_length,
    get_public_key,
)
from hex2words.hex2words import hex2words

from ordinary_portal.config import host, is_testing


def get_super_secret():
    # TODO: replace silly is_testing blocks and OTT comments with unit tests.
    if is_testing:
        super_secret = b"oh yay hi!"
    else:
        super_secret = bytes(input('Enter a super secret message to send securely:'), 'utf-8')
        # TODO: file input option and CLI args
        # super_secret=open("cat.png", "rb").read()
    return super_secret


def generate_pass_phrase():
    # TODO: replace silly is_testing blocks and OTT comments with unit tests.
    if is_testing:
        random_hex = "105bf"
    else:
        random_hex = uuid4().hex[:8]
    pass_phrase_words = hex2words(random_hex).lower()
    return pass_phrase_words


def main():
    """
    Make and print a random pass-phrase
    Spend some CPU cycles to strengthen the key.
    Store a super secret message entered by the user.
    Wait for a message from the recipient, that contains their public key.
    Decode the message using the strengthened key.
    Encrypt the super secret message using the key we just got.
    Send the encrypted message!

    The main difference being how the websocket client is in the middle of it all.
    """

    pass_phrase_words = generate_pass_phrase()

    super_secret = get_super_secret()

    print("Share this key:", pass_phrase_words)

    shared_byte_key = make_key_of_set_length(pass_phrase_words)

    def on_message(connection, unicode_message_text):
        public_key = get_public_key(unicode_message_text, shared_byte_key)
        if not public_key:
            return

        encrypted_payload = encrypt_binary_payload_with_session_key_and_public_key(
            super_secret, public_key
        )
        connection.send(encrypted_payload)  # sent in unicode text format

        connection.close()  # we stop listening, regardless of success or failure

    WebSocketClient(host, on_message=on_message).run_forever()


if __name__ == '__main__':
    main()
