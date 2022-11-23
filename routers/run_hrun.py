from fastapi import APIRouter,Depends
import os,traceback
from loguru import logger

from httprunner import HttpRunner
from httprunner.models import StepResult,TestCaseSummary,TestCase,TStep
from httprunner.loader import load_testcase_file
from httprunner.parser import parse_parameters
from httprunner.step_request import run_step_request,call_hooks

import sys,functools
sys.path.append('..')
from config import Settings

@functools.lru_cache()
def settings():
    return Settings()

router = APIRouter()
runner = HttpRunner()

@router.post("/run_hrun", tags=["httprunner"])
async def run_hrun(testcase_infos: list, config: Settings = Depends(settings)):
    resp = {
        "code": 200,
        "message": "success",
        "results": {}
    }
    try:
        for testcase_info in testcase_infos:
            case_path = testcase_info.get("case_path")
            testcase_json_path = os.path.join(config.ROOT_PATH,case_path)
            if os.path.exists(testcase_json_path):
                summary = run_hrun(case_path)
                if not summary.success:
                    resp["code"] = 300
                    resp["message"] = "httprunner执行异常"
                result = {"summary":summary,"caseID":testcase_info.get("caseID"),"case_path":case_path}
                resp["results"] = result
            else:
                resp["code"] = 400
                resp["message"] = f"Path Not Found:{testcase_json_path}"
    except:
        resp["code"] = 500
        resp["message"] = f"Unexpected Error:{traceback.format_exc()}" 
    return resp

def run_hrun(case_path:str, config: Settings = Depends(settings))->TestCaseSummary:
    testcase_obj = load_testcase_file(os.path.join(config.ROOT_PATH,case_path))
    runner.init_hrun(testcase_obj)
    hrun(testcase_obj)
    summary = runner.get_summary()
    return summary

def hrun(testcase_obj:TestCase):
    if testcase_obj.config.parameters:
        params = parse_parameters(testcase_obj.config.parameters)
        
        for param in params:
            # TODO 参数化执行结果在一个list中
            run_step(testcase_obj,param)
        
    else:
        param = {}
        run_step(testcase_obj,param)

def run_step(testcase_obj:TestCase,param:dict):
    logger.info(f"Start to run testcase: {testcase_obj.config.name}")
    runner.start_time()
    for step in testcase_obj.teststeps:
        if step.request:
            request_step(step,param)
        if step.testcase:
            testcase_step(step)
    runner.total_time()
    logger.info(f"Finished running testcase: {testcase_obj.config.name}")

def request_step(step:TStep,param:dict):
    logger.info(f"run step begin: {step.name} >>>>>>")
    runner.parse_config_variables(param)
    step_result: StepResult = run_step_request(runner,step)
    runner.result_dispose(step_result)
    logger.info(f"run step end: {step.name} <<<<<<\n")
   
def testcase_step(step:TStep, config: Settings = Depends(settings)):
    step_result = StepResult(name=step.name, step_type="testcase")
    step_variables = runner.merge_step_variables(step.variables)
    step_export = step.export
    if step.setup_hooks:
        call_hooks(runner, step.setup_hooks, step_variables, "setup testcase")
    runner.set_referenced().with_session(runner.session).with_case_id(runner.case_id).with_variables(step_variables).with_export(step_export)

    testcase_obj = load_testcase_file(os.path.join(config.ROOT_PATH,step.testcase))
    # parse config variables
    runner.get_config().variables.update(step_variables)
    runner.get_config().variables = runner.parser.parse_variables(testcase_obj.config.variables)
    # parse config name
    runner.get_config().name = runner.parser.parse_data(runner.get_config().name, runner.get_config().variables)
    # parse config base url
    runner.get_config().base_url = runner.parser.parse_data(runner.get_config().base_url, runner.get_config().variables)
    
    hrun(testcase_obj)

    if step.teardown_hooks:
        call_hooks(runner, step.teardown_hooks, step.variables, "teardown testcase")

    summary: TestCaseSummary = runner.get_summary()
    step_result.data = summary.step_results
    step_result.export_vars = summary.in_out.export_vars
    step_result.success = summary.success

    if step_result.export_vars:
        logger.info(f"export variables: {step_result.export_vars}")

if __name__ == "__main__":
    testcase_infos = [{"case_path":"testcases\\a.json","caseID":"case00001"}]
    case_path = testcase_infos[0].get("case_path")
    run_hrun(case_path)

