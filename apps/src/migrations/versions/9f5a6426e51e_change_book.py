"""change book

Revision ID: 9f5a6426e51e
Revises: eb62961236de
Create Date: 2022-02-21 16:47:26.977307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5a6426e51e'
down_revision = 'eb62961236de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    if bind.engine.name not in ['sqlite']:
        op.drop_column('book', 'author')
        op.drop_column('book', 'name')
        op.add_column('book', sa.Column('title', sa.String(length=120), nullable=False))
        op.add_column('book', sa.Column('authors', sa.String(length=120), nullable=False))
        op.add_column('book', sa.Column('publisher', sa.String(length=120), nullable=False))
        op.add_column('book', sa.Column('contents', sa.Text(), nullable=False))
        op.add_column('book', sa.Column('thumbnail', sa.String(length=180), nullable=False))
        op.add_column('book', sa.Column('detailUrl', sa.String(length=180), nullable=False))
        return
    op.rename_table('book', '_book')
    op.create_table('book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('authors', sa.String(length=120), nullable=False),
        sa.Column('publisher', sa.String(length=120), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('thumbnail', sa.String(length=180), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    if bind.engine.name not in ['sqlite']:
        op.drop_column('book', 'detailUrl')
        op.drop_column('book', 'thumbnail')
        op.drop_column('book', 'contents')
        op.drop_column('book', 'publisher')
        op.drop_column('book', 'authors')
        op.drop_column('book', 'title')
        op.add_column('book', sa.Column('name', sa.VARCHAR(length=120), nullable=False))
        op.add_column('book', sa.Column('author', sa.VARCHAR(length=120), nullable=False))
        return
    op.rename_table('book', '_book')
    op.create_table('book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('author', sa.String(length=120), nullable=False),
    )

    # ### end Alembic commands ###