from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.common.tables import notable_accounts_t

app = Flask(__name__)
app.secret_key = settings.ADMIN_SECRET_KEY

app.config['BASIC_AUTH_FORCE'] = settings.ADMIN_BASIC_AUTH_FORCE
app.config['BASIC_AUTH_USERNAME'] = settings.ADMIN_BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = settings.ADMIN_BASIC_AUTH_PASSWORD

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_DSN
app.config['FLASK_ADMIN_SWATCH'] = settings.ADMIN_UI_THEME

basic_auth = BasicAuth(app)
db = SQLAlchemy(app)


class NotableAccount(db.Model):  # type: ignore
    __table__ = notable_accounts_t


class NotableAccountView(ModelView):
    column_display_pk = True
    column_searchable_list = ('address', 'name', 'labels')
    column_filters = ('address', 'name')


admin = Admin(app, name='Jibrel Notable Accounts Admin', template_mode='bootstrap3')
admin.add_view(NotableAccountView(NotableAccount, db.session))
