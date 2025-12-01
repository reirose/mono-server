from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.config import settings
from api.router import cards_router, root_router


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    app_instance.include_router(root_router)
    app_instance.include_router(cards_router)

    yield


app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
