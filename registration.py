from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    create_at: Mapped[datetime] = mapped_column(default=datetime.now)


engine = create_engine('postgresql://localhost:5432/postgres')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def register_user(user_id, username, first_name, last_name):
    user = User(id=user_id, username=username, first_name=first_name, last_name=last_name)
    session.add(user)
    session.commit()
