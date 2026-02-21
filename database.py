# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# db_url = "postgresql://postgres:root@localhost:5432/hospitals"

# engine = create_engine(db_url)



# # Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:root@localhost:5432/hospitals"

engine = create_engine(
    DATABASE_URL,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
