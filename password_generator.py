"""
File: password_generator.py
Description: Handles password generation
Author: Justin Thoreson
Date: 3 January 2024
"""

from hashlib import sha256
from base64 import b64encode
from random import seed, sample, choices, shuffle

class PasswordGenerator(object):
    """Handles password generation."""

    UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    LOWER = 'abcdefghijklmnopqrstuvwxyz'
    NUMBER = '0123456789'
    SPECIAL = '?!@#$%^&*'

    @staticmethod
    def seed(service: str, secret: str, iteration: int):
        """Seeds the pseudorandom generation."""

        composite = ''.join([service, secret, str(iteration)])
        composite_h = PasswordGenerator.__hash(composite)
        seed(composite_h)
    
    @staticmethod
    def generate(
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
        num_each = PasswordGenerator.__ceil_div(min_length, num_components)
        uppers = PasswordGenerator.__sample(PasswordGenerator.UPPER, num_each) if include_upper else ''
        lowers = PasswordGenerator.__sample(PasswordGenerator.LOWER, num_each) if include_lower else ''
        numbers = PasswordGenerator.__sample(PasswordGenerator.NUMBER, num_each) if include_number else ''
        specials = PasswordGenerator.__sample(PasswordGenerator.SPECIAL, num_each) if include_special else ''
        composite = ''.join([uppers, lowers, numbers, specials])
        return PasswordGenerator.__shuffle(composite)

    @staticmethod
    def __hash(data: str) -> str:
        """
        Hashes encoded data.
        :param data: The data to hash
        :return: The hexadecimal string representation of the hashed data
        """

        return sha256(PasswordGenerator.__encode(data)).hexdigest()

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
