from rsa import newkeys as random_key, decrypt as rsa_public_key_decryption
from pyaes import AESModeOfOperationCTR as AESCounterMode

from websocket import WebSocketApp as WebSocketClient
from utils import (
    decrypt_payload_with_session,
    make_key_of_set_length,
    package_binary_as_text,
    unpack_binary_from_safe_ascii,
)
from config import host, is_testing

if is_testing:
    pass_phrase_words = "assume exodus"
else:
    pass_phrase_words = input("Enter shared pass-phrase:").strip()


# Make a stronger key from the weak key, with costly computation
# This key only has a short period to be used
shared_byte_key = make_key_of_set_length(pass_phrase_words)
raw_pub_key, private_key = random_key(1024)
public_key_pack = raw_pub_key.save_pkcs1()
encrypted_public_key = AESCounterMode(shared_byte_key).encrypt(public_key_pack)
our_public_key_encrypted_for_portal_maker = package_binary_as_text(encrypted_public_key)


def decrypt_short_payload(encrypted_text):
    rsa_public_key_decryption(
        unpack_binary_from_safe_ascii(encrypted_text), private_key
    )


def on_message(connection, possible_secure_bundle):
    try:
        amazing_secret = decrypt_payload_with_session(
            possible_secure_bundle, private_key
        )
        connection.close()
        print(amazing_secret)
    except Exception as e:
        pass


def on_open(connection):
    connection.send(our_public_key_encrypted_for_portal_maker)


ws = WebSocketClient(host, on_message=on_message)
ws.on_open = on_open
ws.run_forever()

# make pre-shared key strong (key strengthening / make attacks cost)
# make RSA key pair
# send message with public key
# wait for the big secret
# decode it with private key
