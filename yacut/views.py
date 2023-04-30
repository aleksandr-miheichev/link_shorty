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
    if custom_id and not URLMap.is_short_id_unique(custom_id):
        flash(ID_AVAILABLE.format(custom_id=custom_id))
        return render_template('index.html', form=form)
    existing_link = URLMap.get_by_original_url(original_link)
    if existing_link:
        short_link = f"{base_url}{existing_link.short}"
    else:
        custom_id = URLMap.validate_and_generate_short_id(custom_id)
        URLMap.create_url_map(original_url=original_link, short_id=custom_id)
        short_link = f"{base_url}{custom_id}"
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_view(short_id):
    """
    Перенаправляет пользователей на исходный длинный URL на основе
    предоставленного короткого идентификатора.

    Аргументы:
        - short_id (str): короткий идентификатор, указанный в URL-пути.

    Возвращает:
        - redirect: перенаправление на исходный длинный URL.
        - abort: Ошибка со статусом 404, если короткий идентификатор не найден.
    """
    link = URLMap.get_by_short_id(short_id)
    return redirect(link.original) if link else abort(
        HTTPStatus.NOT_FOUND.value
    )
