from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Antigravity API")

def get_db():
    return database.get_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Antigravity API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
