"""
File: password_manager.py
Description: Generates passwords for different accounts
Author: Justin Thoreson
Date: 3 January 2024
"""

from argparse import ArgumentParser
from hashlib import sha256
from base64 import b64encode
from random import seed, sample, choices, shuffle

class PasswordManager(object):
    """Manages password generation."""

    UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    LOWER = 'abcdefghijklmnopqrstuvwxyz'
    NUMBER = '0123456789'
    SPECIAL = '?!@#$%^&*'

    @staticmethod
    def seed(service: str, secret: str, iteration: int):
        """Seeds the pseudorandom generation."""

        composite = ''.join([service, secret, str(iteration)])
        composite_h = PasswordManager.__hash(composite)
        seed(composite_h)
    
    @staticmethod
    def generate_password(
        min_length: int,
        include_upper: bool = True,
        include_lower: bool = True,
        include_number: bool = True,
        include_special: bool = True
    ) -> str:
        """
        Generates a password.
        :param min_length: The minimum length of the password
        :param upper: Whether to include uppercase letters
        :param lower: Whether to include lowercase letters
        :param number: Whether to include numbers
        :param special: Whether to include special characters
        :return: A generated password
        """

        num_components = include_upper + include_lower + include_number + include_special
        if num_components <= 0:
            raise ValueError('Password must include at least one character type')
        num_each = PasswordManager.__ceil_div(min_length, num_components)
        uppers = PasswordManager.__sample(PasswordManager.UPPER, num_each) if include_upper else ''
        lowers = PasswordManager.__sample(PasswordManager.LOWER, num_each) if include_lower else ''
        numbers = PasswordManager.__sample(PasswordManager.NUMBER, num_each) if include_number else ''
        specials = PasswordManager.__sample(PasswordManager.SPECIAL, num_each) if include_special else ''
        composite = ''.join([uppers, lowers, numbers, specials])
        return PasswordManager.__shuffle(composite)

    @staticmethod
    def __hash(data: str) -> str:
        """
        Hashes encoded data.
        :param data: The data to hash
        :return: The hexadecimal string representation of the hashed data
        """

        return sha256(PasswordManager.__encode(data)).hexdigest()

    @staticmethod
    def __encode(data: str) -> bytes:
        """Encodes data to base 64."""

        data_str = str(data)
        data_utf8 = data_str.encode('UTF-8')
        return b64encode(data_utf8)

    @staticmethod
    def __ceil_div(dividend: int, divisor: int) -> int:
        """Peforms ceiling division."""

        return -(dividend // -divisor)

    @staticmethod
    def __sample(data: str, count: int, allow_duplicates: bool = True) -> str:
        """
        Samples characters from a string pseudorandomly.
        :param data: The string to sample characters from
        :param count: The number of characters to sample
        :param allow_duplicates: Whether duplicate selections are allowed
        """

        selection = choices(data, k=count) if allow_duplicates else sample(data, k=count)
        return ''.join(selection)

    @staticmethod
    def __shuffle(data: str) -> str:
        """Shuffles characters in a string."""

        data_l = list(data)
        shuffle(data_l)
        return ''.join(data_l)

def parse_args() -> tuple:
    """Parses command line arguments."""
    
    arg_parser = ArgumentParser()
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
    arg_parser.add_argument(
        'min_length',
        type=int,
        help='the minimum length of the password'
    )
    arg_parser.add_argument(
        '-u', '--upper',
        action='store_true',
        help='include uppercase letters'
    )
    arg_parser.add_argument(
        '-l', '--lower',
        action='store_true',
        help='include lowercase letters'
    )
    arg_parser.add_argument(
        '-n', '--number',
        action='store_true',
        help='include numbers'
    )
    arg_parser.add_argument(
        '-s', '--special',
        action='store_true',
        help='include special characters'
    )
    return arg_parser.parse_args()

def main() -> None:
    """Runs the password manager program."""

    args = parse_args()
    password_manager = PasswordManager.seed(
        args.service, args.secret, args.iteration)
    try:
        password = PasswordManager.generate_password(
            args.min_length, args.upper, args.lower, args.number, args.special)
    except ValueError as e:
        print(e)
    else:
        print(password)

if __name__ == '__main__':
    main()