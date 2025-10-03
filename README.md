Pequeña API con FastAPI + SQLModel (SQLite). Incluye modelos, DB y endpoints básicos. Aviso: el repo contiene fuerza_bruta.sh (script de ataque). No ejecutes ni subas eso a un repositorio público.

Estructura

main.py — API

schema.py — Pydantic schemas

database.py — engine / sesión

users.py — modelo User

fuerza_bruta.sh — NO usar (eliminar o mantener fuera del repo)

Requisitos

Python 3.10+
Instalar:

pip install fastapi uvicorn sqlmodel sqlalchemy

Ejecutar (desarrollo)
uvicorn main:app --reload
# Documentación: http://127.0.0.1:8000/docs

Endpoints principales

GET / — saludo

POST /login — login (compara username/password en texto plano)

GET /users — lista usuarios

GET /users/id/{id} — usuario por id

POST /users — crear usuario

PUT /users/{id} — actualizar

DELETE /users/{id} — borrar

Nota: hay endpoints/implementaciones peligrosas (ver siguiente sección).
