from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from enum import Enum


class ResponseCode(str, Enum):
    """响应状态码枚举"""

    # 成功状态码
    SUCCESS = "200"
    CREATED = "201"

    # 客户端错误
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    CONFLICT = "409"
    VALIDATION_ERROR = "422"

    # 服务器错误
    INTERNAL_ERROR = "500"
    SERVICE_UNAVAILABLE = "503"


T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """统一响应基础模型"""

    code: str
    data: Optional[T] = None
    msg: str

    class Config:
        json_encoders = {
            # 可以在这里添加自定义编码器
        }


class SuccessResponse(BaseResponse[T]):
    """成功响应模型"""

    def __init__(
        self,
        data: T = None,
        msg: str = "操作成功",
        code: str = ResponseCode.SUCCESS,
        **kwargs,
    ):
        super().__init__(code=code, data=data, msg=msg, **kwargs)


class ErrorResponse(BaseResponse[None]):
    """错误响应模型"""

    def __init__(self, msg: str, code: str = ResponseCode.BAD_REQUEST, **kwargs):
        super().__init__(code=code, data=None, msg=msg, **kwargs)


# 响应工具函数
def success_response(
    data: Any = None, msg: str = "操作成功", code: str = ResponseCode.SUCCESS
) -> BaseResponse:
    """创建成功响应"""
    return BaseResponse(code=code, data=data, msg=msg)


def error_response(msg: str, code: str = ResponseCode.BAD_REQUEST) -> BaseResponse:
    """创建错误响应"""
    return BaseResponse(code=code, data=None, msg=msg)


def created_response(data: Any = None, msg: str = "创建成功") -> BaseResponse:
    """创建资源成功响应"""
    return BaseResponse(code=ResponseCode.CREATED, data=data, msg=msg)


def not_found_response(msg: str = "资源不存在") -> BaseResponse:
    """资源不存在响应"""
    return BaseResponse(code=ResponseCode.NOT_FOUND, data=None, msg=msg)


def unauthorized_response(msg: str = "未授权访问") -> BaseResponse:
    """未授权响应"""
    return BaseResponse(code=ResponseCode.UNAUTHORIZED, data=None, msg=msg)


def forbidden_response(msg: str = "禁止访问") -> BaseResponse:
    """禁止访问响应"""
    return BaseResponse(code=ResponseCode.FORBIDDEN, data=None, msg=msg)


def validation_error_response(msg: str = "数据验证失败") -> BaseResponse:
    """数据验证错误响应"""
    return BaseResponse(code=ResponseCode.VALIDATION_ERROR, data=None, msg=msg)


def internal_error_response(msg: str = "服务器内部错误") -> BaseResponse:
    """服务器内部错误响应"""
    return BaseResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg=msg)
