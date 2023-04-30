from datetime import datetime

from flask import url_for

from yacut.settings import SHORT_LINK_LENGTH
from . import db


class URLMap(db.Model):
    """
    Модель для хранения сопоставления между оригинальными длинными URL и их
    короткими ссылками.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False, index=True)
    short = db.Column(db.String(SHORT_LINK_LENGTH), unique=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view',
                short_id=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
