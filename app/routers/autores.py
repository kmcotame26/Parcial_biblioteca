from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session, init_db
from .. import crud, schemas
from ..models import Autor

router = APIRouter(prefix="/autores", tags=["autores"])

@router.on_event("startup")
async def on_startup():
    await init_db()

@router.post("/", response_model=schemas.AutorRead, status_code=status.HTTP_201_CREATED)
async def crear_autor(data: schemas.AutorCreate, session: AsyncSession = Depends(get_session)) -> Autor:
    return await crud.crear_autor(session, data)

@router.get("/", response_model=List[schemas.AutorRead])
async def listar_autores(
    pais: Optional[str] = Query(default=None, description="Filtrar por país de origen"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.listar_autores(session, pais)

@router.get("/{autor_id}", response_model=schemas.AutorWithLibros)
async def obtener_autor_con_libros(autor_id: int, session: AsyncSession = Depends(get_session)):
    return await crud.obtener_autor_con_libros(session, autor_id)

@router.put("/{autor_id}", response_model=schemas.AutorRead)
async def actualizar_autor(autor_id: int, data: schemas.AutorUpdate, session: AsyncSession = Depends(get_session)):
    return await crud.actualizar_autor(session, autor_id, data)

@router.delete("/{autor_id}", status_code=status.HTTP_200_OK)
async def eliminar_autor(autor_id: int, session: AsyncSession = Depends(get_session)):
    await crud.eliminar_autor(session, autor_id)
    return {"mensaje": "Autor eliminado"}
