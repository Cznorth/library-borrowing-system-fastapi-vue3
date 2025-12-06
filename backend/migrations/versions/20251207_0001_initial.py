from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251207_0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('reader', 'admin', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('isbn', sa.String(length=20), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('publisher', sa.String(length=255), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('tags', sa.String(length=255), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('cover_url', sa.String(length=255), nullable=True),
    )
    op.create_index('ix_books_isbn', 'books', ['isbn'], unique=True)
    op.create_index('ix_books_title', 'books', ['title'])
    op.create_index('ix_books_author', 'books', ['author'])

    op.create_table(
        'book_copies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('barcode', sa.String(length=64), nullable=False),
        sa.Column('shelf_location', sa.String(length=64), nullable=True),
        sa.Column('status', sa.Enum('available', 'loaned', 'retired', name='copystatus'), nullable=False),
    )
    op.create_index('ix_copies_book_id', 'book_copies', ['book_id'])
    op.create_index('uq_copies_barcode', 'book_copies', ['barcode'], unique=True)

    op.create_table(
        'loans',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('copy_id', sa.Integer(), sa.ForeignKey('book_copies.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('loan_date', sa.DateTime(), nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=False),
        sa.Column('return_date', sa.DateTime(), nullable=True),
        sa.Column('renew_count', sa.Integer(), nullable=False, server_default='0'),
    )
    op.create_index('ix_loans_copy_id', 'loans', ['copy_id'])
    op.create_index('ix_loans_user_id', 'loans', ['user_id'])

    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.Enum('queued', 'notified', 'expired', 'canceled', name='reservationstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_reservations_book_id', 'reservations', ['book_id'])
    op.create_index('ix_reservations_user_id', 'reservations', ['user_id'])

    op.create_table(
        'fines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('loan_id', sa.Integer(), sa.ForeignKey('loans.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('status', sa.Enum('unpaid', 'paid', name='finestatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_fines_loan_id', 'fines', ['loan_id'])
    op.create_index('ix_fines_user_id', 'fines', ['user_id'])


def downgrade():
    op.drop_table('fines')
    op.drop_table('reservations')
    op.drop_table('loans')
    op.drop_table('book_copies')
    op.drop_table('books')
    op.drop_table('users')

