# flasknasc

A lightweight minimal-dependency URL shortener in Python. The name comes from `Flask` (the Python microframework) and `nasc` (the Irish for a link).

# Goals

- Make it as easy as possible to setup.
- Fire and forget; require as little maintenance as possible (by scaling to > 1 million links).
- It should be simple to use programmatically.

# Non-Goals

- Performance.
- Ease of adding/onboarding new users.

# Setup

Requires Python3.6+.

1. Install the dependencies (ie. Flask) by running `python3.6 -m pip install -r requirements.txt`.
2. You should create a flasknasc configuration file at `.flasknasc/config.json`. See the "User Configuration" section of this document for an example.

# Usage

A URL mapping consists of a target address, a link ID, and a user prefix. An address like the following:

```
https://flasknasc-address.com/fwd/iandioch/homepage
```

will direct the user to the target address, from the user prefix `iandioch` and the link ID `homepage`.

Each user has a `key`. This is used to authenticate them, so that only they can make new URL mappings with their prefix. This is done by calling the following endpoint:

```
https://flasknasc-address.com/new/iandioch/homepage?key=iandioch_key&address=http://noah.needs.money
```

The key (here `iandioch_key`) will be compared to the stored one, and the mapping will fail if the key is incorrect.

If the key is correct, the link `flasknasc-address.com/fwd/iandioch/homepage` will now redirect visitors to the address `http://noah.needs.money`. The shortened address, relative to the flasknasc host (here the string `/fwd/iandioch/homepage`) will be returned by the endpoint.

The following endpoint can be used to create a new short link with a random ID:

```
https://flasknasc-address.com/new/iandioch?key=iandioch_key&address=http://mycode.doesnot.run
```

Like above, this will return the shortened address if the operation is successful. A shortened address consists of the prefix followed by 12 random alphanumeric characters (eg. `/fwd/iandioch/9ecoafufqmjo`).

# User Configuration

In the flasknasc directory (`.flasknasc`) there should be a file called `config.json`. It should take the following format:

```
{
    "users": [
        {
            "prefix": "iandioch",
            "key": "iandioch_key"
        }
    ]
}
```

To add or remove a user, or to change a user's key, this file should be edited, and flasknasc restarted. Keys are not encrypted.

# Storage

The URL mappings for all users are stored in the same flasknasc directory, with user `iandioch`'s mappings going in a file `.flasknasc/iandioch/links.json`.
