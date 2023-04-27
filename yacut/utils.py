from secrets import choice
from string import ascii_letters, digits

from yacut.models import URLMap
from yacut.settings import DEFAULT_LINK_LENGTH


def random_short_id_generator(length=DEFAULT_LINK_LENGTH):
    """
    Генерирует бесконечный поток случайных коротких идентификаторов
    заданной длины.
    """
    while True:
        yield ''.join(choice(ascii_letters + digits) for _ in range(length))


def is_short_id_unique(short_id):
    """
    Проверяет, является ли заданный короткий идентификатор уникальным в
    таблице URLMap.
    """
    return URLMap.query.filter_by(short=short_id).first() is None


def get_unique_short_id(length=DEFAULT_LINK_LENGTH):
    """Сгенерировать уникальный короткий идентификатор заданной длины."""
    for short_id in random_short_id_generator(length):
        if is_short_id_unique(short_id):
            return short_id
