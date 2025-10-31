from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from .models import Autor, Libro, AutorLibroLink
from . import schemas



async def listar_autores(db: AsyncSession, pais: Optional[str] = None) -> List[Autor]:
    q = select(Autor)
    if pais:
        q = q.where(col(Autor.pais_origen) == pais)
    q = q.order_by(Autor.id)
    return list((await db.execute(q)).scalars().all())

async def obtener_autor(db: AsyncSession, autor_id: int) -> Autor:
    autor = await db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
    return autor

async def obtener_autor_con_libros(db: AsyncSession, autor_id: int) -> Autor:
    return await obtener_autor(db, autor_id)

async def actualizar_autor(db: AsyncSession, autor_id: int, data: schemas.AutorUpdate) -> Autor:
    autor = await obtener_autor(db, autor_id)
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(autor, k, v)
    await db.commit()
    await db.refresh(autor)
    return autor

async def eliminar_autor(db: AsyncSession, autor_id: int) -> None:
    autor = await obtener_autor(db, autor_id)
    await db.delete(autor)
    await db.commit()

async def _validar_isbn_unico(db: AsyncSession, isbn: str, ignore_id: Optional[int] = None) -> None:
    q = select(Libro).where(col(Libro.isbn) == isbn)
    existente = (await db.execute(q)).scalar_one_or_none()
    if existente and existente.id != ignore_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ISBN ya existe")

async def _autores_por_ids(db: AsyncSession, ids: List[int]) -> List[Autor]:
    if not ids:
        return []
    q = select(Autor).where(col(Autor.id).in_(ids))
    encontrados = list((await db.execute(q)).scalars().all())
    if len(encontrados) != len(set(ids)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más autores no existen")
    return encontrados

async def crear_libro(db: AsyncSession, data: schemas.LibroCreate) -> Libro:
    await _validar_isbn_unico(db, data.isbn)
    autores = await _autores_por_ids(db, data.autores_ids)
    libro = Libro(
        titulo=data.titulo,
        isbn=data.isbn,
        anio_publicacion=data.anio_publicacion,
        copias=data.copias,
    )
    libro.autores = autores
    db.add(libro)
    await db.commit()
    await db.refresh(libro)
    return libro

async def listar_libros(db: AsyncSession, anio: Optional[int] = None) -> List[Libro]:
    q = select(Libro)
    if anio is not None:
        q = q.where(col(Libro.anio_publicacion) == anio)
    q = q.order_by(Libro.id)
    return list((await db.execute(q)).scalars().all())

async def obtener_libro(db: AsyncSession, libro_id: int) -> Libro:
    libro = await db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return libro

async def obtener_libro_con_autores(db: AsyncSession, libro_id: int) -> Libro:
    return await obtener_libro(db, libro_id)

async def actualizar_libro(db: AsyncSession, libro_id: int, data: schemas.LibroUpdate) -> Libro:
    libro = await obtener_libro(db, libro_id)
    payload = data.model_dump(exclude_unset=True)


    if "isbn" in payload and payload["isbn"]:
        await _validar_isbn_unico(db, payload["isbn"], ignore_id=libro.id)


    if "copias" in payload and payload["copias"] is not None and payload["copias"] < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las copias no pueden ser negativas")

    for k, v in payload.items():
        if k != "autores_ids":
            setattr(libro, k, v)


    if "autores_ids" in payload and payload["autores_ids"] is not None:
        autores = await _autores_por_ids(db, payload["autores_ids"])
        libro.autores = autores

    await db.commit()
    await db.refresh(libro)
    return libro

async def eliminar_libro(db: AsyncSession, libro_id: int) -> None:
    libro = await obtener_libro(db, libro_id)
    await db.delete(libro)
    await db.commit()
