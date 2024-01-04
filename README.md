# Password Manager

Generates passwords for different services closely conforming to length and character requirements.

## Usage

To generate a password, four input arguments are required:
- `service` - the name of the site or service in which a password is being generated for (string)
- `secret` - a secret phrase or a base password (string)
- `iteration` - how many times this password was generated with the current `service` and `secret` (integer)
- `min_length` - the minimum length of the password to generate (integer)

At least one of the following options are also required:
- `-u, --upper` - include uppercase letters
- `-l, --lower` - include lowercase letters
- `-n, --number` - include numbers
- `-s, --special` - include special characters

Using the `-h, --help` option will display usage details.

`python3 password_manager_v2.py [-h|--help] [-u|--upper] [-l|--lower] [-n|--number] [-s|--special] service secret iteration min_length`

## Example

```
> python3 password_manager_v2.py test-service test-secret 1 12 -ulns
#r%bPF593Yt#
```