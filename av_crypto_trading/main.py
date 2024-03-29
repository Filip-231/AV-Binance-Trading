from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/profit_reports/", response_model=schemas.ProfitReport)
def create_profit_report_for_user(
    user_id: int, item: schemas.ProfitReportCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/profit_reports/", response_model=List[schemas.ProfitReport])
def read_profit_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_profit_reports(db, skip=skip, limit=limit)
    return items


@app.get("/crypto_data/", response_model=List[schemas.Cryptocurrency])
def read_crypto_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crypto_data = crud.get_crypto_data(db, skip=skip, limit=limit)
    return crypto_data
