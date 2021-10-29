from sqlalchemy.orm import Session

import models
import schemas


def get_dealer(db: Session, dealer_id: int):
    return db.query(models.Dealer).filter(models.Dealer.id == dealer_id).first()


def delete_dealer(db: Session, dealer_id: int):
    db.query(models.Dealer).filter(models.Dealer.id == dealer_id).delete()
    db.commit()


def get_dealer_by_email(db: Session, email: str):
    return db.query(models.Dealer).filter(models.Dealer.email == email).first()


def get_dealers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dealer).offset(skip).limit(limit).all()


def create_dealer(db: Session, dealer: schemas.DealerCreate):
    db_dealer = models.Dealer(**dealer.dict())
    db.add(db_dealer)
    db.commit()
    db.refresh(db_dealer)
    return db_dealer


def update_dealer(db: Session, dealer_id: int, dealer: schemas.DealerCreate):
    db_dealer = db.query(models.Dealer).filter(models.Dealer.id == dealer_id)
    db_dealer.update(dealer.dict(exclude_unset=True))
    db.commit()
    db_dealer = db_dealer.first()
    db.refresh(db_dealer)
    return db_dealer


def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()


def get_car(db: Session, vin: int):
    return db.query(models.Car).filter(models.Car.vin == vin).first()


def delete_car(db: Session, vin: int):
    db.query(models.Car).filter(models.Car.vin == vin).delete()
    db.commit()


def create_car(db: Session, car: schemas.CarCreate, dealer_id: int):
    db_car = models.Car(**car.dict(), dealer_id=dealer_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_car(db: Session, vin: int, car: schemas.Car):
    print(car.dict(exclude_unset=True))
    db_car = db.query(models.Car).filter(models.Car.vin == vin)
    db_car.update(car.dict(exclude_unset=True))
    db.commit()
    db_car = db_car.first()
    db.refresh(db_car)
    print(db_car.__dict__)
    return db_car
