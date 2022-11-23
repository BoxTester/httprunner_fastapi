# httprunner_fastapi

#### 介绍
基于httprunnerV4版本的执行服务,使用FastAPI框架对其封装,将接口测试能力对外提供,使其更好地接入测试平台

#### 软件架构
FastAPI

#### 工程目录

- hrun_proj：httprunner工程
- logs：日志
- routers：路由
- utils：工具类
  -httpruner_modify：httprunner二次开发
- config：配置
- main：主程序

#### 使用说明
1. pip install httprunner,将utils/httpruner_modify下的文件替换httprunner库中的文件
2. config配置包含以下配置：
- ROOT_PATH：httprunner工程根目录
- LOG_LEVEL：日志级别    
- EXCUTE_ARGS：pytest执行参数

3. 启动命令：uvicorn main:app
- 打开http://127.0.0.1:8000/docs#,可在fastapi提供的Swagger页面调试对应路由,eg.:
- run_har2case——>"har\\requests.har"
- run_pytest——>"testcases\\requests.json"

#### 路由
1. run_har2case
    将har文件转化为httprunner用例
2. run_pytest
    执行用例,使用pytest的方式执行httprunner用例,得到执行结果
3. run_online_debug
    在线调试,用于接口调试,使用run_har2case转换后的json内容在线执行,得到接口响应结果
