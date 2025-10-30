from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response
from .routers import autores, libros

app = FastAPI(title="Sistema de Gestión de Biblioteca")

app.include_router(autores.router)
app.include_router(libros.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
