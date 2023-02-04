from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#syntax for postgresql
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='api_project',user='postgres',password='root', cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print('Database connected')
#         break
#     except Exception as e:
#         print("Connection failed", e)
#         time.sleep(5)
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()