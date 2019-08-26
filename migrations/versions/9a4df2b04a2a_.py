"""empty message

Revision ID: 9a4df2b04a2a
Revises: 
Create Date: 2019-08-24 21:47:03.979239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a4df2b04a2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaksi',
    sa.Column('id_nota', sa.Integer(), nullable=False),
    sa.Column('id_pembeli', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_nota', 'id_pembeli')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('status_penjual', sa.Boolean(), nullable=False),
    sa.Column('rating', sa.Float(precision=1), nullable=True),
    sa.Column('saldo', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('barang',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_barang', sa.String(length=100), nullable=False),
    sa.Column('id_pemilik', sa.Integer(), nullable=False),
    sa.Column('harga_satuan', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('rating_penjual', sa.Float(), nullable=True),
    sa.Column('url_image', sa.String(length=200), nullable=True),
    sa.Column('deleted_status', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_pemilik'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nota',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_pembeli', sa.Integer(), nullable=False),
    sa.Column('id_barang', sa.Integer(), nullable=False),
    sa.Column('buy_qty', sa.Integer(), nullable=False),
    sa.Column('sub_total', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['id_pembeli'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'id_pembeli', 'id_barang')
    )
    op.create_table('rating',
    sa.Column('id_pembeli', sa.Integer(), nullable=False),
    sa.Column('id_penjual', sa.Integer(), nullable=False),
    sa.Column('given_rating', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['id_pembeli'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_penjual'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_pembeli', 'id_penjual')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    op.drop_table('nota')
    op.drop_table('barang')
    op.drop_table('user')
    op.drop_table('transaksi')
    # ### end Alembic commands ###
