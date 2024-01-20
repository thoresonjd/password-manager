<div align="center">
    <img src="./assets/images/password-manager.jpg", style='border: 5px solid white'>
</div>

Generates and manages passwords for different services closely conforming to length and character requirements.

## Password Generation

Passwords are generated pseudorandomly given a seed, which, therefore, allows passwords to be recovered as long as the same input arguments are provided. To seed the password generator, a string is required. This string is the concatenation of three input fields: the name of the service to generate a password for, a secret phrase, and an iteration, the number of times the current input has been provided (except the iteration itself) to generate a password.

After seeding, a password can be generated. To generate a password, a minimum password length must be provided as well as one to four options. These options determine which type of characters to include in the generated password: uppercase and lowercase letters, digits, and special characters.

The password is guaranteed to include at least one of each character type selected. Thus, the length of the password will be the nearest multiple of the number of options selected rounded up from the minimum length. For example, if a minimum length of one is provided, and all four character types are selected, the password will be four characters long, containing one of each character type.

## Command Line Interface

### Usage

To generate a password, four input arguments are required:
- `service` - the name of the site or service in which a password is being generated for (string)
- `secret` - a secret phrase or a base password (string)
- `iteration` - how many times this password was generated with the current `service` and `secret` (integer)
- `min_length` - the minimum length of the password to generate (integer)

Empty strings are permitted for `service` and `secret`. However, it is advised to provide non-empty data for both, especially `secret`, to amplify the security and uniqueness of each password generated across each individual.

At least one of the following options are also required:
- `-u, --upper` - include uppercase letters
- `-l, --lower` - include lowercase letters
- `-d, --digit` - include digits
- `-s, --special` - include special characters

Using the `-h, --help` option will display usage details.

```
python3 pm_cli.py [-h|--help] [-u|--upper] [-l|--lower] [-d|--digit] [-s|--special] service secret iteration min_length
```

### Example

```
> python3 pm_cli.py test-service test-secret 1 12 -ulds
#r%bPF593Yt#
```

## Graphical User Interface

### Usage

On the right side, echoing the requirements for the [command line interface](#usage), there are four input boxes for the service, secret, iteration, and minimum length, as well as four checkboxes for character type options. Data for the input fields are filled with default arguments: empty strings for the service and secret, which are allowed, and the minimum allowed integer value (1) for the iteration and minimum length. At least one character type must be selected to generate a password.

On the left hand side lies the input log, which lists all unique input used to generate passwords (see [Logging](#logging)). The log can be cleared via the button underneath it.

### Example

<div align="center">
    <img src="./assets/images/gui-example.png">
</div>

## Logging

Whenever a password is generated, the input that generated it is saved to a file named "log" which is accessible in the project's root directory. The file is automatically created if it does not exist when the program is run. This allows for reproducibility of generated passwords, as the passwords themselves are not saved.