from pydantic import BaseSettings

class Settings(BaseSettings):
    ROOT_PATH:str = r"C:\hrp4demo"
    LOG_LEVEL:str = "DEBUG"
    EXCUTE_ARGS:list = ["-sW","ignore:Module already imported:pytest.PytestWarning","--save-tests"]
