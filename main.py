
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/server-info")
def get_server_info():
    return {"version": "1.0.0", "status": "running"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    content = file.file.read()
    return JSONResponse(content={"filename": file.filename, "size": len(content)}, status_code=200)

@app.get("/")
def root():
    return {"message": "Immich-compatible backend running."}

# Seed a default user if not exists
def seed_user():
    db = SessionLocal()
    if db.query(User).count() == 0:
        db.add(User(name="Default User"))
        db.commit()
    db.close()

seed_user()
