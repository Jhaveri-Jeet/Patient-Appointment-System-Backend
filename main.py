from fastapi import FastAPI
from config.database import engine, Base
from routes.patientRoutes import router as patientRoutes
from routes.appointmentRoutes import router as appointmentRoutes
from routes.adminRoutes import router as adminRoutes
import contextlib
from fastapi.middleware.cors import CORSMiddleware


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patientRoutes)
app.include_router(appointmentRoutes)
app.include_router(adminRoutes)
