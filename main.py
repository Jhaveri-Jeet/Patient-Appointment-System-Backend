from fastapi import FastAPI
from config.database import engine, Base
from routes.patientRoutes import router as patientRoutes
import contextlib


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(patientRoutes)
