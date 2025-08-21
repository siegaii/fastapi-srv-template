from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

from app.schemas.base import error_response, ResponseCode


async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    # 根据HTTP状态码映射到我们的响应码
    status_code_mapping = {
        400: ResponseCode.BAD_REQUEST,
        401: ResponseCode.UNAUTHORIZED,
        403: ResponseCode.FORBIDDEN,
        404: ResponseCode.NOT_FOUND,
        409: ResponseCode.CONFLICT,
        422: ResponseCode.VALIDATION_ERROR,
        500: ResponseCode.INTERNAL_ERROR,
        503: ResponseCode.SERVICE_UNAVAILABLE,
    }

    response_code = status_code_mapping.get(
        exc.status_code, ResponseCode.INTERNAL_ERROR
    )
    response = error_response(msg=str(exc.detail), code=response_code)

    return JSONResponse(status_code=exc.status_code, content=response.dict())


async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    """Starlette HTTP异常处理器"""
    status_code_mapping = {
        400: ResponseCode.BAD_REQUEST,
        401: ResponseCode.UNAUTHORIZED,
        403: ResponseCode.FORBIDDEN,
        404: ResponseCode.NOT_FOUND,
        409: ResponseCode.CONFLICT,
        422: ResponseCode.VALIDATION_ERROR,
        500: ResponseCode.INTERNAL_ERROR,
        503: ResponseCode.SERVICE_UNAVAILABLE,
    }

    response_code = status_code_mapping.get(
        exc.status_code, ResponseCode.INTERNAL_ERROR
    )
    response = error_response(msg=str(exc.detail), code=response_code)

    return JSONResponse(status_code=exc.status_code, content=response.dict())


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    # 提取验证错误信息
    error_details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"{field}: {message}")

    error_msg = "数据验证失败: " + "; ".join(error_details)
    response = error_response(msg=error_msg, code=ResponseCode.VALIDATION_ERROR)

    return JSONResponse(status_code=422, content=response.dict())


async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Pydantic验证异常处理器"""
    error_details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"{field}: {message}")

    error_msg = "数据验证失败: " + "; ".join(error_details)
    response = error_response(msg=error_msg, code=ResponseCode.VALIDATION_ERROR)

    return JSONResponse(status_code=422, content=response.dict())


async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    # 记录异常日志（这里可以集成日志系统）
    print(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")

    response = error_response(msg="服务器内部错误", code=ResponseCode.INTERNAL_ERROR)

    return JSONResponse(status_code=500, content=response.dict())
