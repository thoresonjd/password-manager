"""
File: password_manager.py
Description: Generates passwords for different accounts
Author: Justin Thoreson
Date: 27 November 2023
"""

from typing import Any
from argparse import ArgumentParser
from hashlib import sha256, sha512
from base64 import b64encode
from random import seed, randint, choice

class PasswordManager(object):
    """Manages password generation."""

    __slots__ = 'sha'

    def __init__(self, algorithm: int):
        """Initializes the SHA-2 algorithm to use when hashing."""

        if not (algorithm == 256 or algorithm == 512):
            raise ValueError('Unrecognized SHA-2 algorithm')
        self.sha = sha512 if algorithm == 512 else sha256
    
    def generate_password(self, service: str, secret: str, iteration: int) -> str:
        """
        Generates a password.
        :param service: The service in which to generate a password for
        :param secret: A secret phrase
        :param iteration: The number of times this password has been generated
        :return: A generated password
        """

        service_h = self.__hash(service)
        secret_h = self.__hash(secret)
        iteration_h = self.__hash(iteration)
        composite = ''.join([service_h, secret_h, iteration_h])
        composite_h = self.__hash(composite)
        composite_b64str = self.__encode(composite_h).decode()
        composite_trimmed = self.__trimb64(composite_b64str)
        return self.__insert_special_chars(composite_trimmed)

    def __hash(self, data: Any) -> str:
        """
        Hashes encoded data.
        :param data: The data to hash
        :return: The hexadecimal string representation of the hashed data
        """

        return self.sha(self.__encode(data)).hexdigest()

    @staticmethod
    def __encode(data: Any) -> bytes:
        """Encodes data to base 64."""

        data_str = str(data)
        data_utf8 = data_str.encode('UTF-8')
        return b64encode(data_utf8)

    @staticmethod
    def __trimb64(data: str) -> str:
        """Removes the '=' padding from a base 64 string."""

        return data.split('=')[0]

    @staticmethod
    def __insert_special_chars(data: str) -> str:
        """Inserts special characters pseudorandomly into a string."""

        special_chars = list('?!@#$%^&*')
        seed(data)
        num_chars = randint(1, int(len(data) / 2))
        for _ in range(num_chars):
            index = randint(0, len(data) - 1)
            char = choice(special_chars)
            data = ''.join([data[:index], char, data[index:]])
        return data

def parse_args() -> tuple:
    """Parses command line arguments."""
    
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        '-a', '--algorithm',
        type=int,
        choices=[256, 512],
        default=256,
        help='which SHA-2 algorithm to use'
    )
    arg_parser.add_argument(
        'service',
        type=str,
        help='the service in which to generate a password for'
    )
    arg_parser.add_argument(
        'secret',
        type=str, 
        help='a secret phrase'
    )
    arg_parser.add_argument(
        'iteration',
        type=int,
        help='the number of times this password has been generated'
    )
    args = arg_parser.parse_args()
    return args.algorithm, args.service, args.secret, args.iteration

def main() -> None:
    """Runs the password manager program."""

    algorithm, service, secret, iteration = parse_args()
    try:
        password_manager = PasswordManager(algorithm)
    except ValueError as e:
        print(e)
    else:
        password = password_manager.generate_password(service, secret, iteration)
        print(password)

if __name__ == '__main__':
    main()