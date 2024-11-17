from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import uuid

# Variable que tendrá todas las características de una API REST
app = FastAPI()

# Define el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simular base de datos
db = []

# CRUD: Read (lectura) GET ALL: Lee todos los cursos que hay en la lista db
@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
    return db

# CRUD: Create (escribir) POST: agregaremos un nuevo curso a nuestra lista db
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4())
    db.append(curso)
    return curso

# CRUD: Read (lectura) GET (individual): Lee el curso que coincida con el ID que mandemos
@app.get("/cursos/{curso_id}", response_model=Curso)
def optener_curso(curso_id):
    curso = next((curso for curso in db if curso.id == curso_id), None) # Next toma la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD: Update (Actualizar/Modificar) PUT: Modifica el curso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    curso_actualizado.id = curso_id
    index = db.index(curso) # Busca el índice exacto donde está el curso en nuestra lista db
    db[index] = curso_actualizado
    
    return curso_actualizado


# CRUD: Delete (borrado/baja) DELETE: Elimina el curso que coincida con el ID que mandemos
@app.delete("/cursos/id", response_model=Curso)
def eliminar_curso(curso_id):
    curso = next((curso for curso in db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    db.remove(curso)

    return curso