from pydantic import BaseModel, constr
from typing import List, Optional


class CarBase(BaseModel):
    vin: constr(min_length=17, max_length=17, regex=r'^\d+$')
    year: int
    make: str
    model: str
    trim: str
    color: Optional[str] = None
    engine: Optional[str] = None
    seats: Optional[int] = None


class CarCreate(CarBase):
    pass


class CarPatch(BaseModel):
    vin: Optional[int] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    trim: Optional[str] = None
    dealer_id: Optional[int] = None
    color: Optional[str] = None
    engine: Optional[str] = None
    seats: Optional[int] = None


class Car(CarBase):
    dealer_id: int

    class Config:
        orm_mode = True


class DealerBase(BaseModel):
    location: str
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None


class DealerCreate(DealerBase):
    pass


class DealerPatch(BaseModel):
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None


class DealerDelete(BaseModel):
    id: int


class Dealer(DealerBase):
    id: int
    cars: List[Car] = []

    class Config:
        orm_mode = True
