from rsa import newkeys as random_key
from pyaes import AESModeOfOperationCTR as AESCounterMode

from websocket import WebSocketApp as WebSocketClient
from ordinary_portal.utils import (
    decrypt_payload_with_session,
    make_key_of_set_length,
    package_binary_as_text,
)
from ordinary_portal.config import host, is_testing


def download(pass_phrase_words=None):

    # make pre-shared key strong (key strengthening / make attacks cost)
    # make RSA key pair
    # send message with public key
    # wait for the big secret
    # decode it with private key

    if not pass_phrase_words:
        pass_phrase_words = input("Enter shared pass-phrase:").strip()

    shared_byte_key = make_key_of_set_length(
        pass_phrase_words
    )  # Make a stronger key from the weak key
    raw_pub_key, private_key = random_key(1024)
    public_key_pack = raw_pub_key.save_pkcs1()
    encrypted_public_key = AESCounterMode(shared_byte_key).encrypt(public_key_pack)
    our_public_key_encrypted_for_portal_maker = package_binary_as_text(
        encrypted_public_key
    )

    def on_message(connection, possible_secure_bundle):
        try:
            amazing_secret = decrypt_payload_with_session(
                possible_secure_bundle, private_key
            )
            if amazing_secret:
                connection.close()
                try:
                    print(amazing_secret)
                except Exception as e:
                    print("Error printing", str(e))
                file = open("file.bin", "wb")
                file.write(amazing_secret)
                file.close()
        except Exception as e:
            print(e)

    def on_open(connection):
        connection.send(our_public_key_encrypted_for_portal_maker)

    ws = WebSocketClient(host, on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    download()
