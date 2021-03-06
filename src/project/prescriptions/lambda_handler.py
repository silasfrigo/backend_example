from fastapi import FastAPI
from .api.api_v1.api import router
from mangum import Mangum


app = FastAPI(
    title='IClinic Prescriptions API',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
)
app.include_router(router, prefix="/v1")
handler = Mangum(app=app, log_level="error")
