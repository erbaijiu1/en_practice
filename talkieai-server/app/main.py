from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import Config
from app.core.exceptions import UserAccessDeniedException
from app.core.logging import logging
from app.models.response import ApiResponse

from app.api.sys_routes import router as sys_routes
from app.api.account_routes import router as account_routes
from app.api.message_routes import router as message_routes
from app.api.session_routes import router as session_routes
from app.api.topics_route import router as topic_routes
from app.api.words_practice_routes import router as words_practice_routes
from app.utils.logger_config import logger

app = FastAPI()

# Enables CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_routes, prefix=f"{Config.API_PREFIX}/v1")
app.include_router(topic_routes, prefix=f"{Config.API_PREFIX}/v1")
app.include_router(sys_routes, prefix=f"{Config.API_PREFIX}/v1")
app.include_router(session_routes, prefix=f"{Config.API_PREFIX}/v1")
app.include_router(message_routes, prefix=f"{Config.API_PREFIX}/v1")
app.include_router(words_practice_routes, prefix=f"{Config.API_PREFIX}/v1")


@app.exception_handler(Exception)
async def conflict_error_handler(_, exc: Exception):
    """全局异常处理"""
    logging.error(exc)
    # 返回状态码仍为200，exc的错误信息放到ApiResponse中以json格式方式返回并且可以跨域访问
    return JSONResponse(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        content=ApiResponse(code="500", status="FAILED", message=str(exc)).__dict__,
    )


# UserAccessDeniedException异常处理状态码为403
@app.exception_handler(UserAccessDeniedException)
async def user_access_denied_error_handler(_, exc: UserAccessDeniedException):
    """全局异常处理"""
    logging.error(exc)
    # 返回状态码仍为200，exc的错误信息放到ApiResponse中以json格式方式返回并且可以跨域访问
    return JSONResponse(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        content=ApiResponse(code="403", status="FAILED", message=str(exc)).__dict__,
    )


@app.middleware("http")
async def log_all_requests(request: Request, call_next):
    # 基础信息打印
    logger.info(f"[{request.method}] {request.url}")

    # GET参数打印
    if request.method == "GET":
        logger.info(f"GET参数: {dict(request.query_params)}")

    # POST/PUT参数打印（支持JSON/FormData）
    if request.method in ("POST", "PUT", "PATCH"):
        # 读取请求体并缓存（解决body只能读取一次的问题）
        body = await request.body()
        logger.info(f"POST/PUT参数: {body.decode('utf-8')}")

        # # 结构化解析尝试
        # content_type = request.headers.get('content-type', '')
        # try:
        #     if 'application/json' in content_type:
        #         params = await request.json()
        #         logger.info(f"结构化JSON参数: {params}")
        #     elif 'form-data' in content_type:
        #         params = await request.form()
        #         logger.info(f"结构化Form参数: {dict(params)}")
        # except Exception as e:
        #     logger.error(f"参数解析失败: {str(e)}")
        #
        # # 重建请求体（关键步骤）
        # async def receive() -> Message:
        #     return {"type": "http.request", "body": body}

        # request._receive = receive

    response = await call_next(request)
    return response