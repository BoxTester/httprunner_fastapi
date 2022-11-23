from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    ROOT_PATH:str = os.path.abspath("hrun_proj")  
    LOG_LEVEL:str = "DEBUG"
    EXCUTE_ARGS:list = ["-sW","ignore:Module already imported:pytest.PytestWarning","--save-tests"]
