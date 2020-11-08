####################################################################################################

from app.core.config import settings
from app.core.logging import setup_logging
logging_config_file = settings.LOGGING_CONFIG
print('Setup logging using', logging_config_file)
logger = setup_logging(config_file=logging_config_file)

####################################################################################################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router

####################################################################################################

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A portal demo application",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
