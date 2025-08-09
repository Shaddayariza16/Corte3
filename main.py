from fastapi import FastAPI
import mysql.connector
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔹 Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Conexión MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

# 🔹 Modelo Usuario (id_usuario opcional)
class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    usu: str
    contra: str
    correo: str
    nombre: str
    apellido: str
    id_rol: str
    estado: str

# 📌 1️⃣ Listar usuarios
@app.get("/usuarios")
def listar_usuarios():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM usuario")
    result = cursor.fetchall()
    payload = []
    for data in result:
        payload.append({
            "id_usuario": data[0],
            "usu": data[1],
            "contra": data[2],
            "correo": data[3],
            "nombre": data[4],
            "apellido": data[5],
            "id_rol": data[6],
            "estado": data[7]
        })
    return {"resultado": jsonable_encoder(payload)}

# 📌 2️⃣ Crear usuario
@app.post("/usuarios")
def crear_usuario(nuevo_usuario: Usuario):
    cursor = mydb.cursor()
    sql = "INSERT INTO usuario (usu, contra, correo, nombre, apellido, id_rol, estado) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    valores = (nuevo_usuario.usu, nuevo_usuario.contra, nuevo_usuario.correo,
               nuevo_usuario.nombre, nuevo_usuario.apellido, nuevo_usuario.id_rol,
               nuevo_usuario.estado)
    cursor.execute(sql, valores)
    mydb.commit()
    cursor.close()
    return {"mensaje": "Usuario registrado correctamente"}
