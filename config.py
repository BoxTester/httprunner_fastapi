from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    ROOT_PATH:str = os.path.abspath("hrun_proj")  
    LOG_LEVEL:str = "DEBUG"
    HRUN_EXCUTE_ARGS:list = ["hrun","-sW","ignore:Module already imported:pytest.PytestWarning","--save-tests","--log-level",LOG_LEVEL]
