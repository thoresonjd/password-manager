"""
File: pm_cli.py
Description: Manages passwords for different accounts
Author: Justin Thoreson
Date: January 2024
"""

from argparse import ArgumentParser
from password_generator import PasswordGenerator
from logger import Logger

LOG_FILENAME = 'log'
MAX_MIN_LENGTH = 250

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
        '-d', '--digit',
        action='store_true',
        help='include digits'
    )
    arg_parser.add_argument(
        '-s', '--special',
        action='store_true',
        help='include special characters'
    )
    return vars(arg_parser.parse_args()).values()

def log_args(args: tuple) -> None:
    """Logs the provided arguments to a file."""

    def args_to_string(
        service: str, secret: str, iteration: int, min_length: int,
        upper: bool, lower: bool, digit: bool, special: bool
    ) -> str:
        """Creates a string from the input arguments"""

        options = options_to_string(upper, lower, digit, special)
        return ' '.join(
            [service, secret, str(iteration), str(min_length), options]
        )

    def options_to_string(
        upper: bool, lower: bool, digit: bool, special: bool
    ) -> str:
        """Creates a string from the input options."""

        return ''.join(['-',
            ('u' if upper else ''),
            ('l' if lower else ''),
            ('d' if digit else ''),
            ('s' if special else '')])

    log = args_to_string(*args)
    logger = Logger(LOG_FILENAME)
    logger.log_if_not_exists(log)

def main() -> None:
    """Runs the password manager program."""

    args = parse_args()
    service, secret, iteration, min_length, upper, lower, digit, special = args
    composite_seed = ''.join([service, secret, str(iteration)])
    PasswordGenerator.seed(composite_seed)
    try:
        min_length = MAX_MIN_LENGTH if min_length > MAX_MIN_LENGTH else min_length
        password = PasswordGenerator.generate(min_length, upper, lower, digit, special)
    except ValueError as e:
        print(e)
    else:
        print(password)
        log_args(args)

if __name__ == '__main__':
    main()