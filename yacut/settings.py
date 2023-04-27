import os

SHORT_LINK_LENGTH = 16
DEFAULT_LINK_LENGTH = 6
MIN_LINK_LENGTH = 1
INVALID_CHARACTERS = ('Недопустимый символ(ы). Допустимы только буквы, цифры, '
                      'дефисы и знаки подчеркивания.')
LENGTH_ERROR = 'Длина должна быть от 1 до 16 символов.'
RULE = r'^[a-zA-Z0-9\-_]*$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
