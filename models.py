from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint
from db import Base


class TabletProduct(Base):
    __tablename__ = "tablets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    stars_rating = Column(Integer)
    reviews = Column(Integer)
    images = Column(String)
    __table_args__ = (UniqueConstraint("title", name="uq_tablet_title"),)
