from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut.settings import (INVALID_CHARACTERS, LENGTH_ERROR, MIN_LINK_LENGTH,
                            SHORT_LINK_LENGTH, RULE)

ENTER_LONG_LINK = 'Введите длинную ссылку'
MANDATORY_FIELD = 'Обязательное поле'
ENTER_SHORT_LINK = 'Ваш вариант короткой ссылки'
CREATE = 'Создать'


class URLMapForm(FlaskForm):
    """
    Форма для создания коротких URL из длинных URL с необязательным
    пользовательским идентификатором.
    """
    original_link = URLField(
        ENTER_LONG_LINK,
        validators=[DataRequired(message=MANDATORY_FIELD)]
    )
    custom_id = StringField(
        ENTER_SHORT_LINK,
        validators=[
            Optional(),
            Length(MIN_LINK_LENGTH, SHORT_LINK_LENGTH, message=LENGTH_ERROR),
            Regexp(regex=RULE, message=INVALID_CHARACTERS)
        ]
    )
    submit = SubmitField(CREATE)
