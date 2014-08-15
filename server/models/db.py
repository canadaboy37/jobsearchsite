from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:W00t3n@localhost/www', echo=True)

Session = sessionmaker(bind=engine, expire_on_commit=False)