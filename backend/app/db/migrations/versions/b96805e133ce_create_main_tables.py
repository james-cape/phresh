
"""create_main_tables
Revision ID: b96805e133ce
Revises: 
Create Date: 2020-11-15 00:42:05.308632
"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'b96805e133ce'
down_revision = None
branch_labels = None
depends_on = None

def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 5), nullable=False),
        sa.Column("owner", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_cleanings_modtime
            BEFORE UPDATE
            ON cleanings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_users_table() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.Text, unique=True, nullable=False, index=True),
        sa.Column('email', sa.Text, unique=True, nullable=False, index=True),
        sa.Column('email_verified', sa.Boolean, nullable=False, server_default='False'),
        sa.Column('salt', sa.Text, nullable=False),
        sa.Column('password', sa.Text, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='True'),
        sa.Column('is_superuser', sa.Boolean, nullable=False, server_default='False'),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_profiles_table() -> None:
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.Text, nullable=True),
        sa.Column('phone_number', sa.Text, nullable=True),
        sa.Column('bio', sa.Text, nullable=True, server_default=''),
        sa.Column('image', sa.Text, nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_profiles_modtime
            BEFORE UPDATE
            ON profiles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_offers_table() -> None:
    op.create_table(
        'user_offers_for_cleanings',
        sa.Column(
            'user_id',  # 'user' is a reserved word in postgres, so going with user_id instead
            sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column(
            'cleaning_id',  # going with cleaning_id for consistency
            sa.Integer,
            sa.ForeignKey('cleanings.id', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('status', sa.Text, nullable=False, server_default='pending'),
        *timestamps(),
    )
    op.create_primary_key('pk_user_offers_for_cleanings', 'user_offers_for_cleanings', ['user_id', 'cleaning_id'])
    op.execute(
        """
        CREATE TRIGGER update_user_offers_for_cleanings_modtime
            BEFORE UPDATE
            ON user_offers_for_cleanings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_profiles_table()
    create_cleanings_table()
    create_offers_table()


def downgrade() -> None:
    op.drop_table('user_offers_for_cleanings')
    op.drop_table('cleanings')
    op.drop_table('profiles')
    op.drop_table('users')
    op.execute("DROP FUNCTION update_updated_at_column")