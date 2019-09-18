from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from jibrel_notable_accounts import settings

app = Flask(__name__)
app.secret_key = settings.ADMIN_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_DSN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = settings.ADMIN_UI_THEME

db = SQLAlchemy(app)


from jibrel_notable_accounts.admin.model_views import notable_account_view  # NOQA: E402


admin = Admin(app, name='Jibrel Notable Accounts Admin', template_mode='bootstrap3')
admin.add_view(notable_account_view)
