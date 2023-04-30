from datetime import datetime
from re import match
from secrets import choice

from flask import url_for

from yacut.settings import (ALLOWED_CHARACTERS, DEFAULT_LINK_LENGTH,
                            FUNCTION_REDIRECT, MAX_LINK_LENGTH, PATTERN,
                            SIZE_SHORT_USER_ID, UNIQUE_ID_RETRIES)

from . import db
from yacut.error_handlers import InvalidAPIUsage

ID_AVAILABLE_API = 'Имя "{custom_id}" уже занято.'
INVALID_NAME_LINK = 'Указано недопустимое имя для короткой ссылки'


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
                short_id=self.short,
                _external=True
            )
        )

    @staticmethod
    def get_by_original_url(original_url):
        """
        Возвращает экземпляр URLMap, связанный с заданным original_url,
        или None, если он не найден.
        """
        return URLMap.query.filter_by(original=original_url).first()

    @staticmethod
    def get_by_short_id(short_id):
        """
        Возвращает экземпляр URLMap, связанный с заданным short_id, или None,
        если он не найден.
        """
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def is_short_id_unique(short_id):
        """Checks if the given short ID is unique."""
        return URLMap.get_by_short_id(short_id) is None

    @staticmethod
    def _generate_unique_short_id(length=DEFAULT_LINK_LENGTH):
        """Генерирует уникальный короткий идентификатор с указанной длиной."""
        for _ in range(UNIQUE_ID_RETRIES):
            short_id = ''.join(
                choice(ALLOWED_CHARACTERS) for _ in range(length)
            )
            if URLMap.is_short_id_unique(short_id):
                return short_id
        raise ValueError('Не удалось сгенерировать уникальный короткий '
                         'идентификатор после максимального количества '
                         'повторных попыток.')

    @staticmethod
    def validate_and_generate_short_id(custom_id):
        """
        Проверяет предоставленный пользовательский короткий идентификатор,
        генерирует новый, если необходимо, и возвращает окончательный короткий
        идентификатор.
        """
        if custom_id:
            if not match(PATTERN, custom_id) or not (
                    len(custom_id) <= SIZE_SHORT_USER_ID
            ):
                raise InvalidAPIUsage(INVALID_NAME_LINK)
            if URLMap.get_by_short_id(custom_id) is not None:
                raise InvalidAPIUsage(ID_AVAILABLE_API.format(
                    custom_id=custom_id
                ))
        else:
            custom_id = URLMap._generate_unique_short_id()
        return custom_id

    @staticmethod
    def create_url_map(original_url, short_id):
        """
        Создает новый экземпляр URLMap, добавляет его в базу данных и
        возвращает экземпляр.
        """
        urlmap = URLMap(original=original_url, short=short_id)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap
