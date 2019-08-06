"""Add notable accounts table

Revision ID: c6afdb6fb387
Revises:
Create Date: 2019-08-06 10:27:12.315967

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c6afdb6fb387'
down_revision = None
branch_labels = None
depends_on = None


UP_SQL = """
CREATE TABLE notable_accounts (
    address CHARACTER VARYING NOT NULL,
    name CHARACTER VARYING NOT NULL,
    labels CHARACTER VARYING[] NOT NULL
);

ALTER TABLE ONLY notable_accounts
    ADD CONSTRAINT notable_accounts_pkey PRIMARY KEY (address);
"""

DOWN_SQL = """
DROP TABLE notable_accounts;
"""


def upgrade():
    op.execute(UP_SQL)


def downgrade():
    op.execute(DOWN_SQL)
