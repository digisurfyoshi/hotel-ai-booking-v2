from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import models, database, init_db
from .api.routes import auth

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Antigravity API")

@app.on_event("startup")
def on_startup():
    db = database.SessionLocal()
    init_db.init_db(db)
    db.close()

app.include_router(auth.router)
from .api.routes import hotels
app.include_router(hotels.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Antigravity API"}

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    # Simple DB check
    try:
        db.execute("SELECT 1")
    except Exception as e:
        return {"status": "unhealthy", "db_error": str(e)}
    return {"status": "healthy"}
