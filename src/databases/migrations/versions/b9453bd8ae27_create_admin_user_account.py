"""create admin, user, account

Revision ID: b9453bd8ae27
Revises: 13296741ca8f
Create Date: 2025-08-27 05:05:41.868472

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b9453bd8ae27'
down_revision: Union[str, Sequence[str], None] = '13296741ca8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO users (email, hashed_password, first_name, last_name)
        VALUES (
            'testuser@example.com',
            '$2b$12$5Ip76Yos/41C3CYHcXSFiOP7MUF9DNZmTjFrNU4dXGH2KMwMLz4uK',
            'Test',
            'User'
        )
    """)

    op.execute("""
        INSERT INTO administrators (
            email,
            hashed_password,
            first_name,
            last_name
        )
        VALUES (
            'admin@example.com',
            '$2b$12$FwOj/QOY6iGLFBHuRG.7QepcgI098eZKMGCyUyop6X3MaR.17Wx3K',
            'Admin',
            'User'
        )
    """)

    op.execute(
        "INSERT INTO accounts (user_id, balance) VALUES (1, 100)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
