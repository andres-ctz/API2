from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from modelos.users import User
from database import engine, get_session
from sqlmodel import SQLModel
from schemas import UserCreate, UserRead, LoginData


SQLModel.metadata.create_all(engine)

app = FastAPI()




def get_db():
    yield from get_session()


@app.post("/login")
def login(data: LoginData = Body(...), db: Session = Depends(get_session)):
    user = db.query(User).filter(
        User.username == data.username,
        User.password == data.password
    ).first()

    if user:
        return {"mensaje": "acceso verificado, es correcto"}
    else:
        raise HTTPException(status_code=401, detail="usuario incorrecto, no verificado")


# Precargar usuarios
def preload_users():
    with next(get_session()) as db:
        if db.query(User).count() == 0:
            db.add_all([
                User(id=1, username="andres", password="1234"),
                User(id=2, username="juan", password="4321")
            ])
            db.commit()
preload_users()

@app.get("/")
def msg():
    return {"message": "suave"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/id/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/name/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.name == user_name).all()

@app.get("/users/password/{user_password}")
def get_user_by_password(user_password: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.password == user_password).all()


@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = updated_user.name
    user.password = updated_user.password
    db.commit()
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}