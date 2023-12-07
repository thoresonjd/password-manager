# Password Manager

Generates long, scary passwords for different services.

## Usage

To generate a password, three input arguments are required:
- `service` - the name of the site or service in which a password is being generated for (string)
- `secret` - a secret phrase or a base password (string)
- `iteration` - how many times this password was generated with the current `service` and `secret` (integer)

`python3 password_manager.py [service] [secret] [iteration]`

There is one optional argument. The `algorithm` argument can be either `256` or `512` depending on which SHA-2 algorithm is desired during password generation. By default, it is set to `256`.

`python3 password_manager.py --algorithm 512 [service] [secret] [iteration]`