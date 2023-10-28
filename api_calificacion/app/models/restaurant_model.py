from sqlalchemy import Column, Integer, String

from app.database import Base


class Restaurant(Base):
    __tablename__  = "restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    address = Column(String)
