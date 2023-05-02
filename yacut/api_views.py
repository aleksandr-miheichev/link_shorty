from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import PATTERN, SIZE_SHORT_USER_ID

ID_NOT_FOUND = 'Указанный id не найден'
REQUEST_EMPTY = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


@app.route('/api/id/<string:custom_id>/', methods=['GET'])
def get_original_url(custom_id):
    """
    Получить исходный URL, связанный с заданным custom_id.

    Аргументы:
        - custom_id (str): короткий идентификатор для URL.

    Возвращает:
        - (json, int): объект JSON, содержащий исходный URL и код состояния
          HTTP.
    """
    url_map = URLMap.get(custom_id)
    if url_map is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


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
    custom_id = data.get('custom_id') or URLMap.generate_unique_custom_id()
    if custom_id and len(custom_id) > SIZE_SHORT_USER_ID:
        raise InvalidAPIUsage(INVALID_NAME)
    if not PATTERN.match(custom_id):
        raise InvalidAPIUsage(INVALID_NAME)
    return jsonify(
        URLMap.create(data['url'], custom_id).to_dict()
    ), HTTPStatus.CREATED
