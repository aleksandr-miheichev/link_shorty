from http import HTTPStatus

from flask import jsonify, request

from . import app
from yacut.error_handlers import InvalidUsage
from yacut.models import URLMap

ID_NOT_FOUND = 'Указанный id не найден'
REQUEST_EMPTY = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'


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
        raise InvalidUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
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
        raise InvalidUsage(REQUEST_EMPTY)
    if 'url' not in data:
        raise InvalidUsage(URL_REQUIRED_FIELD)
    return jsonify(
        URLMap.create(data['url'], data.get('custom_id')).to_dict()
    ), HTTPStatus.CREATED
