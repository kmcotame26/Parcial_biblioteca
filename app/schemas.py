from typing import Optional, List
from sqlmodel import SQLModel, Field

# -------- AUTOR --------
class AutorCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=120)
    pais_origen: str = Field(min_length=2, max_length=80)
    anio_nacimiento: int = Field(ge=0, le=2100)

class AutorUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    pais_origen: Optional[str] = Field(default=None, min_length=2, max_length=80)
    anio_nacimiento: Optional[int] = Field(default=None, ge=0, le=2100)

class AutorRead(SQLModel):
    id: int
    nombre: str
    pais_origen: str
    anio_nacimiento: int

class LibroMini(SQLModel):
    id: int
    titulo: str
    isbn: str
    anio_publicacion: int
    copias: int

class AutorWithLibros(AutorRead):
    libros: List[LibroMini] = []

# -------- LIBRO --------
class LibroCreate(SQLModel):
    titulo: str = Field(min_length=2, max_length=200)
    isbn: str = Field(min_length=10, max_length=20)
    anio_publicacion: int = Field(ge=0, le=2100)
    copias: int = Field(ge=0)
    autores_ids: List[int] = Field(default_factory=list, description="IDs de autores (coautores)")

class LibroUpdate(SQLModel):
    titulo: Optional[str] = Field(default=None, min_length=2, max_length=200)
    isbn: Optional[str] = Field(default=None, min_length=10, max_length=20)
    anio_publicacion: Optional[int] = Field(default=None, ge=0, le=2100)
    copias: Optional[int] = Field(default=None, ge=0)
    autores_ids: Optional[List[int]] = None  # reemplaza coautores si se envía

class LibroRead(SQLModel):
    id: int
    titulo: str
    isbn: str
    anio_publicacion: int
    copias: int

class AutorMini(SQLModel):
    id: int
    nombre: str
    pais_origen: str

class LibroWithAutores(LibroRead):
    autores: List[AutorMini] = []

