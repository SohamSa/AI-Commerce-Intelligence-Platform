from sqlalchemy.orm import sessionmaker
from database.connection import engine
from database.models import User

SessionLocal = sessionmaker(bind=engine)

def read_users():
    session = SessionLocal()

    users = session.query(User).all()

    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

    session.close()

if __name__ == "__main__":
    read_users()