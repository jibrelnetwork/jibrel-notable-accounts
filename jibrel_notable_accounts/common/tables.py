import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

metadata = sa.MetaData()

notable_accounts_t = sa.Table(
    'notable_accounts',
    metadata,
    sa.Column('address', sa.String, primary_key=True),
    sa.Column('name', sa.String),
    sa.Column('labels', postgresql.ARRAY(sa.String)),
    sa.Column('is_admin_reviewed', sa.Boolean, default=False),
)


TABLES = (
    notable_accounts_t,
)
