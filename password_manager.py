"""
File: password_manager.py
Description: Generates passwords for different accounts
Author: Justin Thoreson
Date: 22 November 2023
"""

from typing import Any
from argparse import ArgumentParser
from hashlib import sha256 as sha
from base64 import b64encode

def parse_args() -> tuple:
    """Parses command line arguments."""
    
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--service', type=str, help='The service in which to generate a password for')
    arg_parser.add_argument('--secret', type=str, help='A secret phrase')
    arg_parser.add_argument('--iteration', type=int, help='The number of times this password has been generated')
    args = arg_parser.parse_args()
    return args.service, args.secret, args.iteration

def encode(data: Any) -> bytes:
    """Encodes data to base 64."""

    data_str = str(data)
    data_utf8 = data_str.encode('UTF-8')
    return b64encode(data_utf8)

def hash(data: Any) -> str:
    """Hashes encoded data."""

    return sha(encode(data)).hexdigest()

def generate_password(service: str, secret: str, iteration: int) -> str:
    """
    Generates a password.
    :param service: The service in which to generate a password for
    :param secret: A secret phrase
    :param iteration: The number of times this password has been generated
    :return: A generated password
    """

    return hash(''.join([hash(service), hash(secret), hash(iteration)]))

def main() -> None:
    """Runs the password manager program."""

    print(generate_password(*parse_args()))

if __name__ == '__main__':
    main()