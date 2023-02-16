from fastapi import FastAPI
import uvicorn
from httprunner.utils import init_logger
from config import Settings

from routers import (
    run_debug,
    run_har2case,
    run_subprocess
)


def create_app():
    init_logger(Settings().LOG_LEVEL)
    app = FastAPI()
    app.include_router(run_har2case.router)
    app.include_router(run_debug.router)
    app.include_router(run_subprocess.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)
