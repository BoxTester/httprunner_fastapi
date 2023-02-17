from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    ROOT_PATH:str = r"C:\hrp4demo" 
    LOG_LEVEL:str = "DEBUG"
    HRUN_EXCUTE_ARGS:list = ["hrun","-sW","ignore:Module already imported:pytest.PytestWarning","--save-tests","--log-level",LOG_LEVEL]
