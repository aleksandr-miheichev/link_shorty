from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from yacut.models import URLMap
from yacut.settings import PATTERN, SIZE_SHORT_USER_ID

INVALID_CHARACTERS = ('Недопустимый символ(ы). Допустимы только буквы, цифры, '
                      'дефисы и знаки подчеркивания.')
LENGTH_ERROR = 'Длина должна быть от 1 до 16 символов.'
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
            Length(max=SIZE_SHORT_USER_ID, message=LENGTH_ERROR),
            Regexp(regex=PATTERN, message=INVALID_CHARACTERS)
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, custom_id):
        if custom_id.data:
            if URLMap.query.filter_by(short=custom_id.data).first():
                raise ValidationError(
                    'Этот короткий идентификатор уже используется. '
                    'Пожалуйста, выберите другой идентификатор.'
                )
