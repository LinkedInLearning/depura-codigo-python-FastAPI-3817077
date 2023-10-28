from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    opinion = Column(String)
    rate = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"), nullable=False)
