from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from .. import crud, schemas
from ..models import Libro

router = APIRouter(prefix="/libros", tags=["libros"])

@router.post("/", response_model=schemas.LibroRead, status_code=status.HTTP_201_CREATED)
async def crear_libro(data: schemas.LibroCreate, session: AsyncSession = Depends(get_session)) -> Libro:
    return await crud.crear_libro(session, data)

@router.get("/", response_model=List[schemas.LibroRead])
async def listar_libros(
    anio: Optional[int] = Query(default=None, description="Filtrar por año de publicación"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.listar_libros(session, anio)

@router.get("/{libro_id}", response_model=schemas.LibroWithAutores)
async def obtener_libro_con_autores(libro_id: int, session: AsyncSession = Depends(get_session)):
    return await crud.obtener_libro_con_autores(session, libro_id)

@router.put("/{libro_id}", response_model=schemas.LibroRead)
async def actualizar_libro(libro_id: int, data: schemas.LibroUpdate, session: AsyncSession = Depends(get_session)):
    return await crud.actualizar_libro(session, libro_id, data)

