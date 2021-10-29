from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Dealer(Base):
    __tablename__ = "dealers"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)

    cars = relationship("Car", back_populates="dealer")


class Car(Base):
    __tablename__ = "cars"
    vin = Column(Integer, primary_key=True, index=True, autoincrement=False)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    trim = Column(String)
    color = Column(String)
    engine = Column(String)
    seats = Column(Integer)
    dealer_id = Column(Integer, ForeignKey('dealers.id'))

    dealer = relationship("Dealer", back_populates="cars")
