from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from registration import User


engine = create_engine('postgresql://localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


def authenticate_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user
