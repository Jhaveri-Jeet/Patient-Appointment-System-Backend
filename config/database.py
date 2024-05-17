from pymysql import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

SYNC_DATABASE_URL = "mysql+pymysql://root:@localhost"
ASYNC_DATABASE_URL = "mysql+aiomysql://root:@localhost/PatientAppointmentSystemDb"

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
try:
    with sync_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS PatientAppointmentSystemDb"))
except OperationalError as e:
    print(f"Error: {e}")

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()
