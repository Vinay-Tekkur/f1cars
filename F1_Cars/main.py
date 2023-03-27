from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Cars(BaseModel):
    id: int
    franchise_name: str = Field(min_length=1)
    driver_names: str = Field(min_length=1)
    ranking: int = Field(gt=0, lt=21)
    engine_made_by: str = Field(min_length=1)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def get_cars_info(db: Session = Depends(get_db)):
    return db.query(models.Cars).all()


@app.get("/cars/{car_id}")
async def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    car_model = db.query(models.Cars).filter(models.Cars.id == car_id).first()
    return car_model


@app.post("/")
async def create_new_car(new_car: Cars, db: Session = Depends(get_db)):
    car_model = models.Cars()

    car_model.franchise_name = new_car.franchise_name
    car_model.driver_names = new_car.driver_names
    car_model.ranking = new_car.ranking
    car_model.engine_made_by = new_car.engine_made_by

    db.add(car_model)
    db.commit()

    return return_status(201)


@app.put("/cars")
async def modify_cars(updated_car: Cars, db: Session = Depends(get_db)):
    car_model = db.query(models.Cars).filter(models.Cars.id == updated_car.id).first()

    car_model.franchise_name = updated_car.franchise_name
    car_model.driver_names = updated_car.driver_names
    car_model.engine_made_by = updated_car.engine_made_by
    car_model.ranking = updated_car.ranking
    db.add(car_model)
    db.commit()

    return return_status(200)

@app.delete("/cars/delete_car/{car_id}")
async def delete_cars(car_id: int, db: Session = Depends(get_db)):
    car_model = db.query(models.Cars).filter(models.Cars.id == car_id).first()
    if car_model is None:
        raise HTTPException(status_code=404, detail="Car Not found!")
    db.query(models.Cars).filter(models.Cars.id == car_id).delete()
    db.commit()

    return return_status(200)

def return_status(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }
