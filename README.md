# httprunner_app

#### 介绍
基于httprunnerV4版本的执行服务，使用FastAPI框架对其封装，将接口测试能力对外提供，使其更好地接入测试平台

#### 软件架构
FastAPI

#### 工程目录

- logs：日志
- project_demo：httprunner工程
- routers：路由
- utils：工具类
  -httpruner_modify：httprunner二次开发
- config：配置
- main：主程序


#### 使用说明
1. pip install httprunner==V4.3，将utils/httpruner_modify下的文件替换httprunner库中的文件
2. config配置包含以下配置：
- ROOT_PATH：httprunner工程根目录
- LOG_LEVEL：日志级别    
- EXCUTE_ARGS：pytest执行参数

3. 启动命令：uvicorn main:app

#### 路由介绍
1. run_har2case
    将har文件转化为httprunner用例
2. run_hrun(V2)
    执行用例，使用json对象的方式执行用例，得到执行结果
3. run_pytest(推荐)
    执行用例，使用pytest的方式执行用例，得到执行结果
4. run_online_debug
    在线调试，使用json用例在线调试，得到接口响应结果
