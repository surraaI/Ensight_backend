import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool
from alembic import context

# Load .env from root
load_dotenv()

# Ensure app/ is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import models and Base
from app.database import Base, DATABASE_URL
from app.models import user, aggregated_news, original_content, enterprise, api_key

# Alembic Config
config = context.config

# Set up Python logging if .ini is present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations without DB connection (generates SQL script)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations with live DB connection."""
    # Modified connection setup for remote PostgreSQL
    engine = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        connect_args={
            "sslmode": "require",  # Enforce SSL
            "keepalives": 1,       # Maintain connection
            "keepalives_idle": 30, # TCP keepalive settings
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    )
    
    with engine.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True  # Enable for enum changes
        )
        with context.begin_transaction():
            context.run_migrations()

# Main switch
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()