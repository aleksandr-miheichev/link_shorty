import random
from datetime import datetime

from flask import url_for

from . import db
from yacut.error_handlers import InvalidUsage
from yacut.settings import (ALLOWED_CHARACTERS, DEFAULT_LINK_LENGTH,
                            FUNCTION_REDIRECT, MAX_LINK_LENGTH, PATTERN,
                            SIZE_SHORT_USER_ID, UNIQUE_ID_RETRIES)

ID_AVAILABLE_API = 'Имя "{custom_id}" уже занято.'
ERROR_CREATE_UNIQUE_CUSTOM_ID = (
    'Не удалось сгенерировать уникальный короткий идентификатор после '
    f'максимального количества повторных попыток - {UNIQUE_ID_RETRIES} раз.'
)
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


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
    def generate_unique_custom_id(length=DEFAULT_LINK_LENGTH):
        """Генерирует уникальный короткий идентификатор с указанной длиной."""
        for _ in range(UNIQUE_ID_RETRIES):
            custom_id = ''.join(random.choices(ALLOWED_CHARACTERS, k=length))
            if URLMap.is_custom_id_unique(custom_id):
                return custom_id
        raise InvalidUsage(ERROR_CREATE_UNIQUE_CUSTOM_ID)

    @staticmethod
    def create(original_url, custom_id=None, validate=True):
        """
        Создаёт новую запись URLMap с заданным original_url и необязательным
        пользовательским custom_id.
        """
        if not custom_id:
            custom_id = URLMap.generate_unique_custom_id()
        else:
            if validate:
                if not URLMap.is_custom_id_unique(custom_id):
                    raise InvalidUsage(ID_AVAILABLE_API.format(
                        custom_id=custom_id
                    ))
                if len(custom_id) > SIZE_SHORT_USER_ID:
                    raise InvalidUsage(INVALID_NAME)
                if not PATTERN.match(custom_id):
                    raise InvalidUsage(INVALID_NAME)
        url_map = URLMap(original=original_url, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map
