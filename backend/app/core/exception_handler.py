from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.core.logger import logger


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    logger.error(
        f"{request.method} {request.url.path} -> {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )