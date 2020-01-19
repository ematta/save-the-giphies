# Database Model

## Users

_id_: int (pk)
_name_: str (default: null)
_email_: str
_password_: str (?)

## Tags

_id_: int
_name_: str (uniq)

## Giphy

_id_: int
_user_: int (fk: Users.id)
_giphy_: str (giphy id)
_tag_: int (Tags.id)

# Installation

`psycopg2` needs `apt-get install libpq-dev python-dev` on ubuntu and `brew install postgres` on mac. For mac, add the following to your direnv .envrc file

```
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```