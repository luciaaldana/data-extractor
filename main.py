import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    logger.info("The root endpoint (/) was called.")
    return {"message": "The backend is running correctly"}
