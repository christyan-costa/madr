"""criando tabela de romancistas

Revision ID: c18df1a0ad89
Revises: bd568a6ccc12
Create Date: 2024-08-17 15:21:18.854406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c18df1a0ad89'
down_revision: Union[str, None] = 'bd568a6ccc12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Using batch mode to add the foreign key constraint in SQLite
    with op.batch_alter_table('books') as batch_op:
        batch_op.create_foreign_key(
            'fk_books_romancistas', 
            'romancistas', 
            ['romancista_id'], 
            ['id']
        )

def downgrade():
    # Using batch mode to drop the foreign key constraint if needed
    with op.batch_alter_table('books') as batch_op:
        batch_op.drop_constraint('fk_books_romancistas', type_='foreignkey')

