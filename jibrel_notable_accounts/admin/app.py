from typing import List

from flask import Flask
from flask_admin import Admin
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.admin.database_queries import update_is_admin_reviewed_true, update_is_admin_reviewed_false
from jibrel_notable_accounts.common.tables import notable_accounts_t

app = Flask(__name__)
app.secret_key = settings.ADMIN_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_DSN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = settings.ADMIN_UI_THEME

db = SQLAlchemy(app)


class NotableAccount(db.Model):  # type: ignore
    __table__ = notable_accounts_t


class NotableAccountView(ModelView):
    column_display_pk = True
    column_searchable_list = ('address', 'name', 'labels')
    column_filters = ('address', 'name')

    @action('review', 'Review', 'Are you sure you want to review selected accounts?')
    def review_accounts(self, ids: List[str]):
        with db.engine.connect() as conn:
            conn.execute(update_is_admin_reviewed_true(ids))

    @action('unreview', 'Unreview', 'Are you sure you want to unreview selected accounts?')
    def unreview_accounts(self, ids: List[str]):
        with db.engine.connect() as conn:
            conn.execute(update_is_admin_reviewed_false(ids))


admin = Admin(app, name='Jibrel Notable Accounts Admin', template_mode='bootstrap3')
admin.add_view(NotableAccountView(NotableAccount, db.session))
