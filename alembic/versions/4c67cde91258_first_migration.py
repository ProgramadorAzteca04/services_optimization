"""first migration

Revision ID: 4c67cde91258
Revises: 
Create Date: 2025-05-06 13:01:28.107853
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c67cde91258'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('campaigns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('state', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('credentials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('indexing_id', sa.Integer(), nullable=True),  # <- FK agregada después
        sa.Column('last_reset', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('indexing',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('credential_id', sa.Integer(), nullable=True),  # <- también opcional
        sa.Column('link_page', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Agregar FK manualmente después para romper el ciclo
    op.create_foreign_key(
        "fk_indexing_credential",
        "indexing", "credentials",
        ["credential_id"], ["id"]
    )

    op.create_foreign_key(
        "fk_credential_indexing",
        "credentials", "indexing",
        ["indexing_id"], ["id"]
    )

    op.create_table('design_elements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('service', sa.String(), nullable=False),
        sa.Column('number', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('layout', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('alt_name', sa.String(), nullable=False),
        sa.Column('local_city', sa.String(), nullable=False),
        sa.Column('local_state', sa.String(), nullable=False),
        sa.Column('postal_code', sa.String(), nullable=False),
        sa.Column('wizard', sa.String(), nullable=False),
        sa.Column('meta', sa.String(), nullable=False),
        sa.Column('channel_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_design_elements_id'), 'design_elements', ['id'], unique=False)

    op.create_table('domains',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.Column('admin', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('scheduled',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('title_seo', sa.String(), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('key_phrase', sa.String(), nullable=True),
        sa.Column('url', sa.String(length=512), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('total_reviews', sa.Integer(), nullable=True),
        sa.Column('blocks', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('services',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('services_name', sa.String(), nullable=False),
        sa.Column('services_slug', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('services')
    op.drop_table('scheduled')
    op.drop_table('domains')
    op.drop_index(op.f('ix_design_elements_id'), table_name='design_elements')
    op.drop_table('design_elements')
    op.drop_constraint("fk_credential_indexing", "credentials", type_="foreignkey")
    op.drop_constraint("fk_indexing_credential", "indexing", type_="foreignkey")
    op.drop_table('indexing')
    op.drop_table('credentials')
    op.drop_table('campaigns')
