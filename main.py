"""
File: main.py
Description: Manages passwords for different accounts
Author: Justin Thoreson
Date: 3 January 2024
"""

from argparse import ArgumentParser
from password_generator import PasswordGenerator
from logger import Logger

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
    return vars(arg_parser.parse_args()).values()

def main() -> None:
    """Runs the password manager program."""

    args = parse_args()
    service, secret, iteration, min_length, upper, lower, number, special = args 
    PasswordGenerator.seed(service, secret, iteration)
    try:
        password = PasswordGenerator.generate(min_length, upper, lower, number, special)
    except ValueError as e:
        print(e)
    else:
        print(password)
        characters = ''.join(['-',
            ('u' if upper else ''),
            ('l' if lower else ''),
            ('n' if number else ''),
            ('s' if special else '')])
        log = ' '.join([service, secret, str(iteration), str(min_length), characters])
        logger = Logger('log')
        logger.log_if_not_exists(log)

if __name__ == '__main__':
    main()