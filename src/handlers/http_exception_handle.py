from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class HttpExceptionHandler:
    @staticmethod
    def handler(request: Request, exception: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code, content={"message": exception.detail}
        )
