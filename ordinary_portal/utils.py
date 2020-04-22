import json
from base64 import b16decode as decoder
from base64 import b16encode as ascii_subset
from hashlib import sha256

import rsa
from pyaes import AESModeOfOperationCTR as AESCounterMode
from rsa import PublicKey as PublicKeyHandler

rounds = int(10000000 / 4)


def package_binary_as_text(byte_array):
    # TODO: be less hacky
    return str(ascii_subset(byte_array)).replace("b'", "").replace("'", "")


def unpack_binary_from_safe_ascii(ascii_byte_array):
    return decoder(str.encode(ascii_byte_array))


def make_key_of_set_length(anything):
    """Make 256 bit (32 byte) key from anything"""

    ha = sha256()
    # TODO: consider pyscrypt or similar
    for costly_computational_round in range(rounds):
        try:
            ha.update(str.encode(anything))
        except:
            ha.update(anything)
    return ha.digest()


def encrypt_binary_payload_with_session_key_and_public_key(payload, public_key):
    """Expects a binary payload format"""
    raw_session_key = make_key_of_set_length(rsa.randnum.read_random_bits(32))[:32]
    encrypted_session_key = rsa.encrypt(raw_session_key, public_key)
    session_encrypted_payload = AESCounterMode(raw_session_key).encrypt(payload)
    bundle = json.dumps(
        dict(
            encrypted_session_key=package_binary_as_text(encrypted_session_key),
            session_encrypted_payload=package_binary_as_text(session_encrypted_payload),
        )
    )
    return bundle


def decrypt_payload_with_session(payload_as_text, private_key):
    bundle = json.loads(payload_as_text)
    encrypted_session_key = unpack_binary_from_safe_ascii(
        bundle["encrypted_session_key"]
    )  # just for me
    session_encrypted_payload = unpack_binary_from_safe_ascii(
        bundle["session_encrypted_payload"]
    )
    session_key = rsa.decrypt(encrypted_session_key, private_key)
    decrypted_payload_binary = AESCounterMode(session_key).decrypt(
        session_encrypted_payload
    )
    return decrypted_payload_binary


def get_public_key(possible_public_key_response_from_peer, shared_byte_key):
    try:
        bytes_again = unpack_binary_from_safe_ascii(
            possible_public_key_response_from_peer
        )
        # Decode using public key:
        public_key_pack = AESCounterMode(shared_byte_key).decrypt(bytes_again)
        # Unpack the key from it's pkcs1 wrapper:
        public_key = PublicKeyHandler.load_pkcs1(public_key_pack)
        return public_key
    except Exception as e:
        print("decrypt fail", e)
        return None