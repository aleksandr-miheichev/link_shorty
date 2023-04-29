from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request
from sqlalchemy import or_

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .settings import ID_AVAILABLE
from .utils import get_unique_short_id

SHORT_LINK = ('<p><b>Ваша новая ссылка готова:</b><br>'
              '<a href="{base_url}{short_link}" target="_blank">'
              '{base_url}{short_link}</a></p>')


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Страница с формой для создания сокращённых ссылок.

    Возвращает:
        - render_template:  Рендерит шаблон 'quick_link.html' с формой и
          любыми флэш-сообщениями.
    """
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        original_link = form.original_link.data
        base_url = request.url_root
        existing_link = URLMap.query.filter(or_(
            URLMap.original == original_link,
            URLMap.short == custom_id
        )).first()
        if existing_link:
            if existing_link.original == original_link:
                flash(SHORT_LINK.format(
                    base_url=base_url,
                    short_link=existing_link.short
                ))
            else:
                flash(ID_AVAILABLE.format(custom_id=custom_id))
        else:
            if not custom_id:
                custom_id = get_unique_short_id()
            db.session.add(URLMap(original=original_link, short=custom_id))
            db.session.commit()
            flash(SHORT_LINK.format(base_url=base_url, short_link=custom_id))
    return render_template('quick_link.html', form=form)


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
    link = URLMap.query.filter_by(short=short_id).first()
    return redirect(link.original) if link else abort(
        HTTPStatus.NOT_FOUND.value
    )
