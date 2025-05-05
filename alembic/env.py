import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Додаємо корінь проєкту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db import Base
from models import TabletProduct

# Завантажуємо змінні середовища
load_dotenv()

# Це об'єкт конфігурації Alembic
config = context.config

# Встановлюємо sqlalchemy.url зі змінних середовища
config.set_section_option(
    "alembic",
    "sqlalchemy.url",
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost:5432/{os.getenv('DB_NAME')}",
)

# Налаштовуємо логери з конфігураційного файлу
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Встановлюємо метадані для автогенерації міграцій
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
