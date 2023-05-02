from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from yacut.models import URLMap
from yacut.settings import MAX_LINK_LENGTH, PATTERN, SIZE_SHORT_USER_ID

INVALID_CHARACTERS = ('Недопустимый символ(ы). Допустимы только буквы, цифры, '
                      'дефисы и знаки подчеркивания.')
LENGTH_ERROR = 'Длина должна быть до {max_length_user_id} символов.'
ENTER_LONG_LINK = 'Введите длинную ссылку'
MANDATORY_FIELD = 'Обязательное поле'
ENTER_SHORT_LINK = 'Ваш вариант короткой ссылки'
CREATE = 'Создать'
ID_AVAILABLE = 'Имя {custom_id} уже занято!'
LINK_LIMIT_LENGTH = 'Длина ссылки должна быть до {max_link_length} символов'


class URLMapForm(FlaskForm):
    """
    Форма для создания коротких URL из длинных URL с необязательным
    пользовательским идентификатором.
    """
    original_link = URLField(
        ENTER_LONG_LINK,
        validators=[
            DataRequired(message=MANDATORY_FIELD),
            Length(max=MAX_LINK_LENGTH, message=LINK_LIMIT_LENGTH.format(
                max_link_length=MAX_LINK_LENGTH
            ))
        ]
    )
    custom_id = StringField(
        ENTER_SHORT_LINK,
        validators=[
            Optional(),
            Length(max=SIZE_SHORT_USER_ID, message=LENGTH_ERROR.format(
                max_length_user_id=SIZE_SHORT_USER_ID
            )),
            Regexp(regex=PATTERN.pattern, message=INVALID_CHARACTERS)
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, custom_id):
        if custom_id.data:
            if not URLMap.is_custom_id_unique(custom_id.data):
                raise ValidationError(ID_AVAILABLE.format(
                    custom_id=custom_id.data
                ))
