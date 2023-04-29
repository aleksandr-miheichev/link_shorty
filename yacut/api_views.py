from http import HTTPStatus
from re import match

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import (ID_AVAILABLE_API, INVALID_NAME_LINK, MIN_LINK_LENGTH,
                       RULE, SHORT_LINK_LENGTH)
from .utils import get_unique_short_id, is_short_id_unique

ID_NOT_FOUND = 'Указанный id не найден'
REQUEST_EMPTY = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    Получить исходный URL, связанный с заданным short_id.

    Аргументы:
        - short_id (str): короткий идентификатор для URL.

    Возвращает:
        - (json, int): объект JSON, содержащий исходный URL и код состояния
          HTTP.
    """
    original_link = URLMap.query.filter_by(short=short_id).first()
    if original_link is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND.value)
    return jsonify(original_link.to_dict()), HTTPStatus.OK.value


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """
    Создает новую короткую ссылку для заданного URL.

    Возвращает:
        - (json, int): объект JSON, содержащий созданное соответствие
          короткого идентификатора URL и оригинальной ссылки, а также код
          статуса HTTP.
    """
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(REQUEST_EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD)
    custom_id = data.get('custom_id')
    if custom_id:
        if not match(RULE, custom_id):
            raise InvalidAPIUsage(INVALID_NAME_LINK)
        if not (MIN_LINK_LENGTH <= len(custom_id) <= SHORT_LINK_LENGTH):
            raise InvalidAPIUsage(INVALID_NAME_LINK)
        if not is_short_id_unique(custom_id):
            raise InvalidAPIUsage(ID_AVAILABLE_API.format(custom_id=custom_id))
    else:
        custom_id = get_unique_short_id()
        data['custom_id'] = custom_id
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({'urlmap': urlmap.to_dict()}), HTTPStatus.CREATED.value
