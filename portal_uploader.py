from uuid import uuid4

from rsa import encrypt as rsa_encrypt_to_public_key
from rsa import PublicKey as PublicKeyHandler
from pyaes import AESModeOfOperationCTR as AESCounterMode

from websocket import WebSocketApp as WebSocketClient
from utils import (
    encrypt_binary_payload_with_session_key_and_public_key,
    make_key_of_set_length,
    package_binary_as_text,
    unpack_binary_from_safe_ascii,
)
from hex2words.hex2words import hex2words

from config import host, is_testing

# exclusive_secret = bytes(input('message to send:'),'utf-8')
exclusive_secret = b"oh yay hi!"
# exclusive_secret=open("cat.png", "rb").read()

if is_testing:
    random_hex = "105bf"
else:
    random_hex = uuid4().hex[:8]

pass_phrase_words = hex2words(random_hex)
shared_byte_key = make_key_of_set_length(pass_phrase_words)

print("Share this key:", pass_phrase_words)


def get_public_key(possible_public_key_response_from_peer):
    try:
        bytes_again = unpack_binary_from_safe_ascii(
            possible_public_key_response_from_peer
        )
        public_key_pack = AESCounterMode(shared_byte_key).decrypt(bytes_again)
        public_key = PublicKeyHandler.load_pkcs1(public_key_pack)
        return public_key
    except Exception as e:
        print("decrypt fail", e)
        return None


def encrypt_short_binary_secret_with_public_key(public_key):
    try:
        super_secret = rsa_encrypt_to_public_key(exclusive_secret, public_key)
        b_secret = package_binary_as_text(super_secret)
        print("Sent, closing")
        return b_secret
    except Exception as e:
        print("Failed to encrypt", e)


def on_message(connection, unicode_message_text):
    public_key = get_public_key(unicode_message_text)
    if not public_key:
        connection.close()
        return

    # encrypted_payload_packaged_as_text = encrypt_short_binary_secret_with_public_key(public_key)
    encrypted_payload_packaged_as_text = encrypt_binary_payload_with_session_key_and_public_key(
        exclusive_secret, public_key
    )
    connection.send(encrypted_payload_packaged_as_text)
    connection.close()  # we stop listening, regardless of success or failure


WebSocketClient(host, on_message=on_message,).run_forever()
