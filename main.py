from fastapi import FastAPI
import uvicorn
from httprunner.utils import init_logger
from config import Settings

from routers import (
    run_pytest,
    run_har2case,
    run_online_debug
)


def create_app():
    init_logger(Settings().LOG_LEVEL)
    app = FastAPI()
    app.include_router(run_pytest.router)
    app.include_router(run_har2case.router)
    app.include_router(run_online_debug.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
