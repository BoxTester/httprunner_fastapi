from fastapi import APIRouter
import traceback

from loguru import logger

from utils.http_request import HttpRequest

router = APIRouter()

@router.post("/run_online_debug", tags=["requests"])
async def run_online_debug(testcase_infos: dict):
    resp = {
        "code": 200,
        "message": "success",
        "results": {}
    }
    try:
        request_info = testcase_infos.get("teststeps")[0].get("request")
        method = request_info.get("method")
        url = request_info.get("url")
        kwargs = {}
        if request_info.get("headers"):
            kwargs['headers'] = request_info.get("headers")
        if request_info.get("cookies"):
            kwargs['cookies'] = request_info.get("cookies")
        if request_info.get("data"):
            kwargs['data'] = request_info.get("data")
        if request_info.get("json"):
            kwargs['json'] = request_info.get("json")
        if request_info.get("params"):
            kwargs['params'] = request_info.get("params")
        if request_info.get("upload"):
            kwargs['files'] = request_info.get("upload")
        req_resp = HttpRequest().request(method, url, **kwargs)
        resp["results"] = req_resp
    except:
        resp["code"] = 500
        resp["message"] = f"Unexpected Error:{traceback.format_exc()}"
    logger.debug(resp["message"])
    return resp
