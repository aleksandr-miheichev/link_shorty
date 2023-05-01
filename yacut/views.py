from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from . import app
from .forms import URLMapForm
from .models import URLMap

ID_AVAILABLE = 'Имя {custom_id} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Страница с формой для создания сокращённых ссылок.

    Возвращает:
        - render_template:  Рендерит шаблон 'index.html' с формой и любыми
          флэш-сообщениями.
    """
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    original_link = form.original_link.data
    base_url = request.url_root
    if custom_id and not URLMap.is_custom_id_unique(custom_id):
        flash(ID_AVAILABLE.format(custom_id=custom_id))
        return render_template('index.html', form=form)
    new_url_map = URLMap.create(
        original_url=original_link,
        custom_id=custom_id
    )
    short_link = f"{base_url}{new_url_map.short}"
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_view(custom_id):
    """
    Перенаправляет пользователей на исходный длинный URL на основе
    предоставленного короткого идентификатора.

    Аргументы:
        - custom_id (str): короткий идентификатор, указанный в URL-пути.

    Возвращает:
        - redirect: перенаправление на исходный длинный URL.
        - abort: Ошибка со статусом 404, если короткий идентификатор не найден.
    """
    link = URLMap.get(custom_id)
    return redirect(link.original) if link else abort(
        HTTPStatus.NOT_FOUND
    )
