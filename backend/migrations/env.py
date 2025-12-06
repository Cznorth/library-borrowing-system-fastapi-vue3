from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys
import os

config = context.config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.db import Base  # noqa
from app.models.user import User  # noqa
from app.models.book import Book  # noqa
from app.models.book_copy import BookCopy  # noqa
from app.models.loan import Loan  # noqa
from app.models.reservation import Reservation  # noqa
from app.models.fine import Fine  # noqa


target_metadata = Base.metadata

def run_migrations_offline():
    url = os.environ.get("SQLALCHEMY_DATABASE_URI") or config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    section = config.get_section(config.config_ini_section)
    env_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if env_url:
        section["sqlalchemy.url"] = env_url
    connectable = engine_from_config(section, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

