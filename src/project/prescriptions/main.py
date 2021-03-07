from fastapi import FastAPI
from .api.api_v1.api import router
from mangum import Mangum
from prescriptions.models import prescription
from connections import engine


prescription.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='IClinic Prescriptions API',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
)
app.include_router(router, prefix="/v1")
handler = Mangum(app=app, log_level="error")
