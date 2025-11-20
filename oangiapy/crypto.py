import hashlib
import base64
import json
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_public_key
    
class Crypto:

    # ---------------- MD5 ----------------
    @staticmethod
    def md5(text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    # ---------------- RSA ----------------
    @staticmethod
    def generate_rsa_keypair(key_size: int = 2048) -> tuple:
        """Generate RSA public/private key pair in PEM format."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pub_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pub_pem, priv_pem

    @staticmethod
    def rsa_encrypt(data: dict, pub_key_b64: str) -> str:
        pub_bytes = base64.b64decode(pub_key_b64)  # decode Base64 DER
        pub_key = load_der_public_key(pub_bytes)   # load as DER
        plaintext = json.dumps(data).encode()
        cipher = pub_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(cipher).decode()

    @staticmethod
    def rsa_decrypt(cipher_b64: str, priv_key_pem: bytes) -> dict:
        priv_key = serialization.load_pem_private_key(priv_key_pem, password=None, backend=default_backend())
        cipher_bytes = base64.b64decode(cipher_b64)
        plaintext = priv_key.decrypt(
            cipher_bytes,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return json.loads(plaintext.decode())

    # ---------------- AES ----------------
    @staticmethod
    def generate_aes_key(key_size: int = 32) -> bytes:
        """
        Generate a random AES key.
        key_size: 16 (AES-128), 24 (AES-192), 32 (AES-256)
        """
        return os.urandom(key_size)

    @staticmethod
    def aes_encrypt(data: dict, key: bytes) -> dict:
        plaintext = json.dumps(data).encode()
        padder = sym_padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return {
            "iv": base64.b64encode(iv).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode()
        }

    @staticmethod
    def aes_decrypt(encrypted_data: dict, key: bytes) -> dict:
        iv = base64.b64decode(encrypted_data["iv"])
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return json.loads(plaintext.decode())
