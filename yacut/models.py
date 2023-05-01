from datetime import datetime
from secrets import choice

from flask import url_for

from yacut.settings import (ALLOWED_CHARACTERS, DEFAULT_LINK_LENGTH,
                            FUNCTION_REDIRECT, MAX_LINK_LENGTH,
                            SIZE_SHORT_USER_ID, UNIQUE_ID_RETRIES)

from . import db
from yacut.error_handlers import InvalidAPIUsage

ID_AVAILABLE_API = 'Имя "{custom_id}" уже занято.'
INVALID_NAME_LINK = 'Указано недопустимое имя для короткой ссылки'
ERROR_CREATE_UNIQUE_CUSTOM_ID = ('Не удалось сгенерировать уникальный '
                                 'короткий идентификатор после максимального '
                                 'количества повторных попыток.')


class URLMap(db.Model):
    """
    Модель для хранения сопоставления между оригинальными длинными URL и их
    короткими ссылками.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(MAX_LINK_LENGTH),
        nullable=False,
        index=True
    )
    short = db.Column(db.String(SIZE_SHORT_USER_ID), unique=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Преобразует экземпляр URLMap в словарь."""
        return dict(
            url=self.original,
            short_link=url_for(
                FUNCTION_REDIRECT,
                custom_id=self.short,
                _external=True
            )
        )

    @staticmethod
    def get(custom_id):
        """
        Возвращает экземпляр URLMap, связанный с заданным custom_id, или None,
        если он не найден.
        """
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def is_custom_id_unique(custom_id):
        """
        Проверяет, является ли заданный короткий идентификатор уникальным.
        """
        return URLMap.get(custom_id) is None

    @staticmethod
    def _generate_unique_custom_id(length=DEFAULT_LINK_LENGTH):
        """Генерирует уникальный короткий идентификатор с указанной длиной."""
        for _ in range(UNIQUE_ID_RETRIES):
            custom_id = ''.join(
                choice(ALLOWED_CHARACTERS) for _ in range(length)
            )
            if URLMap.is_custom_id_unique(custom_id):
                return custom_id
        raise ValueError(ERROR_CREATE_UNIQUE_CUSTOM_ID)

    @staticmethod
    def create(original_url, custom_id=None):
        """
        Создаёт новую запись URLMap с заданным original_url и необязательным
        пользовательским custom_id.
        """
        if custom_id:
            if not len(custom_id) <= SIZE_SHORT_USER_ID:
                raise InvalidAPIUsage(INVALID_NAME_LINK)
            if all(char in ALLOWED_CHARACTERS for char in custom_id):
                raise InvalidAPIUsage(INVALID_NAME_LINK)
            if URLMap.get(custom_id) is not None:
                raise InvalidAPIUsage(
                    ID_AVAILABLE_API.format(custom_id=custom_id)
                )
        else:
            custom_id = URLMap._generate_unique_custom_id()
        url_map = URLMap(original=original_url, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map
