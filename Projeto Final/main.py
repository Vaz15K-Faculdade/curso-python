from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from db.database import create_db_and_tables
from db.events_database import create_events_db_and_tables
from db.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()  # Banco de usuários
    await create_events_db_and_tables()  # Banco de eventos e tickets
    yield

app = FastAPI(
    title="Tessera API",
    description="API para Tessera — sistema de ingressos",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Tessera API",
        "description": "API para Tessera — sistema de ingressos",
        "version": "1.0.0",
        "frontend": "Use o aplicativo desktop ou o frontend para acessar a interface do Tessera"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)