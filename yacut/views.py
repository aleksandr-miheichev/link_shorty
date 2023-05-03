from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .error_handlers import InvalidUsage
from .forms import URLMapForm
from .models import URLMap
from .settings import FUNCTION_REDIRECT


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
    try:
        return render_template(
            'index.html',
            form=form,
            short_link=url_for(
                FUNCTION_REDIRECT,
                custom_id=URLMap.create(
                    original_url=original_link,
                    custom_id=custom_id
                ).short,
                _external=True
            )
        )
    except InvalidUsage as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<string:custom_id>', methods=['GET'])
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
    url_map = URLMap.get(custom_id)
    return redirect(url_map.original) if url_map else abort(
        HTTPStatus.NOT_FOUND
    )
