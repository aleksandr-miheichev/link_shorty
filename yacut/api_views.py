from http import HTTPStatus

from flask import jsonify, request

from . import app
from yacut.error_handlers import InvalidAPIUsage, InvalidORMUsage
from yacut.models import URLMap
from yacut.settings import MAX_LINK_LENGTH

ID_NOT_FOUND = 'Указанный id не найден'
REQUEST_EMPTY = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
ID_AVAILABLE_API = 'Имя "{custom_id}" уже занято.'
LINK_LIMIT_LENGTH = f'Длина ссылки должна быть до {MAX_LINK_LENGTH} символов'


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
    try:
        created_url_map = URLMap.create(data['url'], data.get('custom_id'))
        return jsonify(created_url_map.to_dict()), HTTPStatus.CREATED
    except InvalidORMUsage as e:
        if str(e) == INVALID_NAME:
            raise InvalidAPIUsage(INVALID_NAME)
        elif str(e) == LINK_LIMIT_LENGTH:
            raise InvalidAPIUsage(LINK_LIMIT_LENGTH)
        elif str(e) == ID_AVAILABLE_API.format(
                custom_id=data.get('custom_id')
        ):
            raise InvalidAPIUsage(
                ID_AVAILABLE_API.format(custom_id=data.get('custom_id'))
            )
        else:
            raise InvalidAPIUsage(str(e))
