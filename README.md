# Password Manager

Generates long, scary passwords for different services.

## Usage

To generate a password, three input arguments are required:
- `service` - the name of the site or service in which a password is being generated for (string)
- `secret` - a secret phrase or a base password (string)
- `iteration` - how many times this password was generated with the current `service` and `secret` (integer)

There is one optional argument. The `algorithm` (`a`) argument can be either `256` or `512` depending on which SHA-2 algorithm is desired during password generation. By default, it is set to `256`.

Using the `-h, --help` option will display usage details.

`python3 password_manager_v1.py [-h|--help] [-a|--algorithm {256,512}] service secret iteration`

## Example

```
> python3 password_manager_v1.py test-service test-secret 1
NW%MzZmZm@@Y2$E!?!0YjM0Y2Fl%MTB%jM$TY4MzcyY2&E2ZTQwMzFjOTc5YzRmMTc1NjQyYz&Q?!2@&^@?N#T*E3NTdhY2RmMDB^!@hZDQ2Ng
```