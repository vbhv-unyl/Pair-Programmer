# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

Base = declarative_base()

# Create async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=False)

# Async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency for FastAPI routes
async def get_db():
    async with async_session() as session:
        yield session

# ---------------------------
# Async function to create tables
# ---------------------------
async def init_db():
    """
    Create all tables in the database.
    Call this at startup in development.
    """
    async with engine.begin() as conn:
        # Run synchronous metadata.create_all in async context
        await conn.run_sync(Base.metadata.create_all)
