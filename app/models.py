from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ---- Tabla enlace N:M ----
class AutorLibroLink(SQLModel, table=True):
    __tablename__ = "autores_libros"
    autor_id: Optional[int] = Field(default=None, foreign_key="autores.id", primary_key=True)
    libro_id: Optional[int] = Field(default=None, foreign_key="libros.id", primary_key=True)

# ---- Autor ----
class AutorBase(SQLModel):
    nombre: str = Field(index=True, min_length=2, max_length=120)
    pais_origen: str = Field(index=True, min_length=2, max_length=80)
    anio_nacimiento: int = Field(ge=0, le=2100)

class Autor(AutorBase, table=True):
    __tablename__ = "autores"
    id: Optional[int] = Field(default=None, primary_key=True)
    libros: List["Libro"] = Relationship(back_populates="autores", link_model=AutorLibroLink)

# ---- Libro ----
class LibroBase(SQLModel):
    titulo: str = Field(index=True, min_length=2, max_length=200)
    isbn: str = Field(index=True, min_length=10, max_length=20, description="ISBN único")
    anio_publicacion: int = Field(ge=0, le=2100)
    copias: int = Field(ge=0, description="Número de copias disponibles (>= 0)")

class Libro(LibroBase, table=True):
    __tablename__ = "libros"
    id: Optional[int] = Field(default=None, primary_key=True)
    autores: List[Autor] = Relationship(back_populates="libros", link_model=AutorLibroLink)
