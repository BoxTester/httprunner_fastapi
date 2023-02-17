import os,traceback,json,functools
from loguru import logger

from fastapi import APIRouter,Depends
import subprocess

from config import Settings
@functools.lru_cache()
def settings():
    return Settings()

router = APIRouter()

@router.post("/run_subprocess", tags=["httprunner"])
async def run_subprocess(testcase_info: dict, config: Settings = Depends(settings)):
    logger.info(f"run_subprocess.params: {testcase_info}")
    resp = {
        "code": 200,
        "message": "success",
        "results": {}
    }
    try:
        case_path = testcase_info.get("case_path")
        testcase_json_path = os.path.join(config.ROOT_PATH,case_path)
        if os.path.exists(testcase_json_path):
            excute_args = []
            excute_args.extend(config.HRUN_EXCUTE_ARGS)
            excute_args.append(testcase_json_path)
            CompletedProcess = subprocess.run(excute_args)
            summary_path = os.path.join(config.ROOT_PATH, "logs",f"{case_path.split('.')[0]}.summary.json")
            if os.path.exists(summary_path):
                with open(summary_path,"r") as summary_file:
                    summary = json.load(summary_file)
                resp["results"] = {"summary":summary,"caseID":testcase_info.get("caseID"),"case_path":case_path}
                os.remove(summary_path)
                if CompletedProcess.returncode != 0:
                    error_path = os.path.join("logs","httprunner.exceptions.log")
                    if os.path.exists(error_path):
                        with open(error_path,"r") as error_file:
                            message = error_file.read()
                        os.remove(error_path)
                    else:
                        message = "httprunner.exceptions: Unexpected Error"
                    resp["code"] = 300
                    resp["message"] = message
            else:
                resp["code"] = 400
                resp["message"] = f"Summary Not Generated:{summary_path}"
        else:
            resp["code"] = 400
            resp["message"] = f"Path Not Exist:{testcase_json_path}"
    except:
        resp["code"] = 500
        resp["message"] = f"Unexpected Error:{traceback.format_exc()}"
    logger.info("run_subprocess.return: "+resp["message"])
    return resp
