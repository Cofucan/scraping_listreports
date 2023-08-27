"""
This module defines logic for encrypting and decrypting files containing
sensitive information such as passwords and API keys. The files are first
encrypted before being pushed to a remote server, where they can be pulled
and decrypted from another computer.
"""
import os
import sys

from cryptography.fernet import Fernet


def generate_key(keyfile: str = "key.key") -> bytes:
    """
    Generate an encryption key and save it securely.

    Args:
        keyfile (str): the name and path of the key file to be saved

    Returns:
        A 32-byte random key that can be used to encrypt and decrypt data.
    """
    key = Fernet.generate_key()

    # Store the key securely in a file
    with open(keyfile, "wb") as key_file:
        key_file.write(key)

    return key


def load_key(keyfile: str = "key.key") -> bytes:
    """
    Load an encryption key from a file.

    Args:
        keyfile (str): the name and path of the key file to be loaded

    Returns:
        A 32-byte random key that can be used to encrypt and decrypt data.
    """
    with open(keyfile, "rb") as key_file:
        key = key_file.read()

    return key


# Encrypt a file
def encrypt_file(file_path: str, encrypt_key: bytes) -> None:
    """
    Encrypts a file, using an encryption key.

    Args:
        file_path (str): The path to the file to be encrypted
        encrypt_key (bytes): The encryption key
    """
    with open(file_path, "rb") as file:
        plaintext = file.read()

    fernet = Fernet(encrypt_key)
    encrypted_data = fernet.encrypt(plaintext)

    with open(f"{file_path}.enc", "wb") as file:
        file.write(encrypted_data)


# Decrypt a file
def decrypt_file(file_path: str, encrypt_key: bytes) -> None:
    """
    Decrypts a file, using an encryption key.

    Args:
        file_path (str): The path to the file to be decrypted
        encrypt_key (bytes): The encryption key
    """
    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    fernet = Fernet(encrypt_key)
    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path.replace(".enc", ""), "wb") as file:
        file.write(decrypted_data)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        generate_key()
        print("Key file generated successfully in current directory!")
        sys.exit(0)

    if len(sys.argv) != 4:
        sys.exit(f"Incorrect number of arguments.\n\n{sys.argv}")

    if sys.argv[1] not in ["--encrypt", "--decrypt"]:
        sys.exit(
            f"Invalid argument: {sys.argv[1]}.\nPlease specifiy '--encrypt'"
            " or '--decrypt'."
        )

    if not os.path.exists(sys.argv[2]):
        sys.exit(
            f"File not found: {sys.argv[2]}.\nPlease specify a valid file."
        )

    if not os.path.exists(sys.argv[3]):
        sys.exit(
            f"Key file not found: {sys.argv[3]}.\nPlease specify a valid"
            " encryption key file."
        )

    FLAG = sys.argv[1]
    FILE = sys.argv[2]
    KEYFILE = sys.argv[3]

    encryption_key = load_key(KEYFILE)

    if FLAG == "--decrypt":
        decrypt_file(FILE, encryption_key)
    elif FLAG == "--encrypt":
        encrypt_file(FILE, encryption_key)

    # ENCRYPTION_KEY = b'...'  # Load the encryption key from a secure source
    # encrypt_file('options.ini', ENCRYPTION_KEY)
    # encrypt_file('emails.json', ENCRYPTION_KEY)
    # decrypt_file('options.ini', ENCRYPTION_KEY)
    # decrypt_file('emails.json', ENCRYPTION_KEY)
