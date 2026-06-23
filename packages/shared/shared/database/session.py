from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.settings import settings


engine = create_engine(
    settings.postgres_url,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)