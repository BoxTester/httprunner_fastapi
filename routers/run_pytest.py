import os,traceback,json,sys
from loguru import logger

from fastapi import APIRouter,Depends
from httprunner.cli import main_run

import functools
sys.path.append('..')
from config import Settings

@functools.lru_cache()
def settings():
    return Settings()

router = APIRouter()

@router.post("/run_pytest", tags=["httprunner"])
async def run_pytest(testcase_info: dict, config: Settings = Depends(settings)):
    logger.info(f"run_pytest.params: {testcase_info}")
    resp = {
        "code": 200,
        "message": "success",
        "results": {}
    }
    try:
        case_path = testcase_info.get("case_path")
        testcase_json_path = os.path.join(config.ROOT_PATH,case_path)
        if os.path.exists(testcase_json_path):
            excute_args = config.EXCUTE_ARGS
            excute_args.append(testcase_json_path)
            exit_code = main_run(excute_args)
            summary_path = os.path.join(config.ROOT_PATH, "logs",f"{case_path.split('.')[0]}.summary.json")
            with open(summary_path,"r") as summary_file:
                summary = json.load(summary_file)
            if exit_code != 0:
                error_path = os.path.join("logs","httprunner.exceptions.log")
                if os.path.exists(error_path):
                    with open(error_path,"r") as error_file:
                        message = error_file.read()
                    os.remove(error_path)
                else:
                    message = "httprunner.exceptions: Unexpected Error"
                resp["code"] = 300
                resp["message"] = message
            result = {"summary":summary,"caseID":testcase_info.get("caseID"),"case_path":case_path}
            resp["results"] = result
        else:
            resp["code"] = 400
            resp["message"] = f"Path Not Exist:{testcase_json_path}"
    except:
        resp["code"] = 500
        resp["message"] = f"Unexpected Error:{traceback.format_exc()}"
    logger.info("run_pytest.return: "+resp["message"])
    return resp
