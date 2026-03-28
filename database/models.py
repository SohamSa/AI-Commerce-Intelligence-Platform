from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from database.connection import engine

Base = declarative_base()


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    stage = Column(String)


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)


class AudienceSegment(Base):
    __tablename__ = "audience_segments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age_group = Column(String)
    interest = Column(String)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


if __name__ == "__main__":
    create_tables()