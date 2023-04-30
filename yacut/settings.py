import os

SHORT_LINK_LENGTH = 16
DEFAULT_LINK_LENGTH = 6
MIN_LINK_LENGTH = 1
INVALID_CHARACTERS = ('Недопустимый символ(ы). Допустимы только буквы, цифры, '
                      'дефисы и знаки подчеркивания.')
LENGTH_ERROR = 'Длина должна быть от 1 до 16 символов.'
RULE = r'^[A-Za-z0-9]{1,6}$'
INVALID_NAME_LINK = 'Указано недопустимое имя для короткой ссылки'
ID_AVAILABLE = 'Имя {custom_id} уже занято!'
ID_AVAILABLE_API = 'Имя {custom_id} уже занято.'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SECRET_KEY = os.getenv('SECRET_KEY')
