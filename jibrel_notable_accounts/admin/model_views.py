from typing import List

from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView

from jibrel_notable_accounts.admin.app import db
from jibrel_notable_accounts.admin.database_queries import update_is_admin_reviewed_true, update_is_admin_reviewed_false
from jibrel_notable_accounts.common.tables import notable_accounts_t


class NotableAccount(db.Model):  # type: ignore
    __table__ = notable_accounts_t


class NotableAccountView(ModelView):
    column_display_pk = True
    column_searchable_list = ('address', 'name')
    column_sortable_list = ('address', 'name', 'labels', 'is_admin_reviewed')

    column_default_sort = [('name', True), ('address', True)]
    column_filters = ('address', 'name', 'is_admin_reviewed')

    can_set_page_size = True

    form_columns = ('address', 'name', 'labels', 'is_admin_reviewed')

    @action('review', 'Review', 'Are you sure you want to review selected accounts?')
    def review_accounts(self, ids: List[str]) -> None:
        with db.engine.connect() as conn:
            conn.execute(update_is_admin_reviewed_true(ids))

    @action('unreview', 'Unreview', 'Are you sure you want to unreview selected accounts?')
    def unreview_accounts(self, ids: List[str]) -> None:
        with db.engine.connect() as conn:
            conn.execute(update_is_admin_reviewed_false(ids))


notable_account_view = NotableAccountView(NotableAccount, db.session)  # type: ignore
