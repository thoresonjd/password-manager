"""
File: password_manager.py
Description: Generates passwords for different accounts
Author: Justin Thoreson
Date: 22 November 2023
"""

from typing import Any
from argparse import ArgumentParser
from hashlib import sha256, sha512
from base64 import b64encode
from random import seed, randint, choice

def parse_args() -> tuple:
    """Parses command line arguments."""
    
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        '--algorithm',
        type=int,
        choices=[256, 512],
        default=256,
        help='Which SHA-2 algorithm to use'
    )
    arg_parser.add_argument(
        'service',
        type=str,
        help='The service in which to generate a password for'
    )
    arg_parser.add_argument(
        'secret',
        type=str, 
        help='A secret phrase'
    )
    arg_parser.add_argument(
        'iteration',
        type=int,
        help='The number of times this password has been generated'
    )
    args = arg_parser.parse_args()
    return args.algorithm, args.service, args.secret, args.iteration

def encode(data: Any) -> bytes:
    """Encodes data to base 64."""

    data_str = str(data)
    data_utf8 = data_str.encode('UTF-8')
    return b64encode(data_utf8)

def hash(algorithm: int, data: Any) -> str:
    """
    Hashes encoded data.
    :param algorithm: Which SHA-2 algorithm to use
    :param data: The data to hash
    :return: The hexadecimal string representation of the hashed data
    """

    sha = sha512 if algorithm == 512 else sha256
    return sha(encode(data)).hexdigest()

def insertSpecialChars(data: str) -> str:
    """Inserts special characters pseudorandomly into a string."""

    special_chars = ['?', '!', '@', '#', '$', '%']
    seed(data)
    num_chars = randint(1, int(len(data) / 2))
    for _ in range(num_chars):
        index = randint(0, len(data) - 1)
        char = choice(special_chars)
        data = ''.join([data[:index], char, data[index:]]) 
    return data

def generate_password(
    algorithm: int, service: str, secret: str, iteration: int
) -> str:
    """
    Generates a password.
    :param algorithm: Which SHA-2 algorithm to use
    :param service: The service in which to generate a password for
    :param secret: A secret phrase
    :param iteration: The number of times this password has been generated
    :return: A generated password
    """

    service_h = hash(algorithm, service)
    secret_h = hash(algorithm, secret)
    iteration_h = hash(algorithm, iteration)
    composite = ''.join([service_h, secret_h, iteration_h])
    composite_h = hash(algorithm, composite)
    composite_b64str = encode(composite_h).decode()
    return insertSpecialChars(composite_b64str)

def main() -> None:
    """Runs the password manager program."""

    print(generate_password(*parse_args()))

if __name__ == '__main__':
    main()