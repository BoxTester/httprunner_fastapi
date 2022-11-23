from fastapi import APIRouter
import os,traceback
from loguru import logger

from har2case.core import HarParser

router = APIRouter()

@router.post("/run_har2case", tags=["har2case"])
async def run_har2case(har_path: str):
    logger.info(f"run_har2case.params: {har_path}")
    resp = {
        "code": 200,
        "message": "success",
        "results": {}
    }
    try:
        if os.path.exists(har_path):
            case_info = HarParser(har_path)._make_testcase("V2")
            result = {"case_info":case_info,"har_path":har_path}
            resp["results"] = result
        else:
            resp["code"] = 400
            resp["message"] = f"Path Not Exist:{har_path}"
    except:
        resp["code"] = 500
        resp["message"] = f"Unexpected Error:{traceback.format_exc()}"  
    logger.info("run_har2case.return:"+resp["message"])    
    return resp
    

if __name__ == "__main__":
    har_path = 'C:\\hrp4demo\\har\\test.har'
    print(HarParser(har_path)._make_testcase("V2"))
