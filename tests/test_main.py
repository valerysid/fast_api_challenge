from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from database import Base
from main import app, get_db

os.remove('./test.db')
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


fake_dealer = {
    "location": "US",
    "phone": "+180011111111",
    "email": "info@copart.com",
    "website": "http://copart.com"
}

fake_car = {
    "vin": "12345678912345678",
    "year": 2020,
    "make": "Audi",
    "model": "A4",
    "trim": "Premium",
    "color": "white",
    "engine": "2L",
    "seats": 4
}


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_dealer():
    response = client.post(
        "/dealers/",
        json=fake_dealer
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == fake_dealer["email"]
    assert "id" in data
    user_id = data["id"]
    fake_dealer["id"] = user_id

    response = client.get(f"/dealers/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == fake_dealer["email"]
    assert data["id"] == user_id


def test_read_dealers():
    response = client.get("/dealers/")
    assert response.status_code == 200, response.text
    data = response.json()
    fake_dealer['cars'] = []
    assert data == [fake_dealer]


def test_update_dealer():
    updated_dealer = {
        'location': 'CA',
        'phone': fake_dealer['phone'],
        'email': fake_dealer['email'],
        'website': fake_dealer['website'],
    }

    response = client.put(f"/dealers/{fake_dealer['id']}", json=updated_dealer)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['location'] == updated_dealer["location"]


def test_patch_dealer():
    updated_phone = {'phone': '+380982122479'}

    response = client.patch(f"/dealers/{fake_dealer['id']}", json=updated_phone)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['phone'] == updated_phone["phone"]


def test_create_car():
    response = client.post(f"/dealers/{fake_dealer['id']}/cars/", json=fake_car)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["vin"] == fake_car["vin"]

    response = client.get(f"/cars/{data['vin']}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["make"] == fake_car["make"]


def test_create_bad_vin_car():
    bad_car = {**fake_car, 'vin': '1234'}
    response = client.post(f"/dealers/{fake_dealer['id']}/cars/", json=bad_car)
    assert response.status_code == 422, response.text
    data = response.json()


def test_read_cars():
    response = client.get("cars")
    assert response.status_code == 200, response.text
    data = response.json()
    fake_car['dealer_id'] = fake_dealer['id']
    assert data == [fake_car]


def test_update_car():
    updated_car = {**fake_car, 'model': 'A5'}
    response = client.put(f"/cars/{fake_car['vin']}", json=updated_car)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['model'] == updated_car['model']


def test_patch_car():
    car_patch = {
        'year': 2021
    }

    response = client.patch(f"/cars/{fake_car['vin']}", json=car_patch)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['year'] == car_patch['year']


def test_delete_car():
    response = client.delete(f"/cars/{fake_car['vin']}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {}

    response = client.get(f"/cars/{fake_car['vin']}")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Car not found'


def test_delete_dealer():
    response = client.delete(f"/dealers/{fake_dealer['id']}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {}

    response = client.get(f"/dealers/{fake_dealer['id']}")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Dealer not found'
