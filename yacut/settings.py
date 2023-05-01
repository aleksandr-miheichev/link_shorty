import os
from string import ascii_letters, digits
import re

UNIQUE_ID_RETRIES = 10
ALLOWED_CHARACTERS = ascii_letters + digits
SIZE_SHORT_USER_ID = 16
MAX_LINK_LENGTH = 2048
DEFAULT_LINK_LENGTH = 6
PATTERN = re.compile(f"^[{ALLOWED_CHARACTERS}]+$")
FUNCTION_REDIRECT = 'redirect_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SECRET_KEY = os.getenv('SECRET_KEY')
