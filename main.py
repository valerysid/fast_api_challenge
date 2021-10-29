from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dealers/", response_model=schemas.Dealer)
def create_dealer(dealer: schemas.DealerCreate, db: Session = Depends(get_db)):
    db_dealer = crud.get_dealer_by_email(db, email=dealer.email)
    if db_dealer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_dealer(db=db, dealer=dealer)


@app.get("/dealers/", response_model=List[schemas.Dealer])
def read_dealers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dealers = crud.get_dealers(db, skip=skip, limit=limit)
    return dealers


@app.get("/dealers/{dealer_id}", response_model=schemas.Dealer)
def read_dealer(dealer_id: int, db: Session = Depends(get_db)):
    db_dealer = crud.get_dealer(db, dealer_id=dealer_id)
    if db_dealer is None:
        raise HTTPException(status_code=404, detail="Dealer not found")
    return db_dealer


@app.delete("/dealers/{dealer_id}")
def delete_dealer(dealer_id: int, db: Session = Depends(get_db)):
    db_dealer = crud.get_dealer(db, dealer_id=dealer_id)
    if db_dealer is None:
        raise HTTPException(status_code=404, detail="Dealer not found")
    crud.delete_dealer(db, dealer_id=dealer_id)
    return {}


@app.put("/dealers/{dealer_id}", response_model=schemas.Dealer)
def update_dealer(dealer_id: int, dealer: schemas.DealerCreate, db: Session = Depends(get_db)):
    db_dealer = crud.get_dealer(db, dealer_id=dealer_id)
    if db_dealer is None:
        raise HTTPException(status_code=404, detail="Dealer not found")

    db_dealer = crud.update_dealer(db, dealer_id=dealer_id, dealer=dealer)
    return db_dealer


@app.patch("/dealers/{dealer_id}", response_model=schemas.Dealer)
def patch_dealer(dealer_id: int, dealer: schemas.DealerPatch, db: Session = Depends(get_db)):
    db_dealer = crud.get_dealer(db, dealer_id=dealer_id)
    if db_dealer is None:
        raise HTTPException(status_code=404, detail="Dealer not found")

    db_dealer = crud.update_dealer(db, dealer_id=dealer_id, dealer=dealer)
    return db_dealer


@app.post("/dealers/{dealer_id}/cars/", response_model=schemas.Car)
def create_car(
    dealer_id: int, car: schemas.CarCreate, db: Session = Depends(get_db)
):
    return crud.create_car(db=db, car=car, dealer_id=dealer_id)


@app.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_cars(db, skip=skip, limit=limit)
    return items


@app.get("/cars/{vin}", response_model=schemas.Car)
def read_car(vin: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, vin=vin)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return db_car


@app.put("/cars/{vin}", response_model=schemas.Car)
def update_car(vin: int, car: schemas.Car, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, vin=vin)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db_car = crud.update_car(db, vin=vin, car=car)
    return db_car


@app.patch("/cars/{vin}", response_model=schemas.Car)
def patch_car(vin: int, car: schemas.CarPatch, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, vin=vin)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db_car = crud.update_car(db, vin=vin, car=car)
    return db_car


@app.delete("/cars/{vin}")
def delete_car(vin: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, vin=vin)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    crud.delete_car(db, vin=vin)
    return {}
