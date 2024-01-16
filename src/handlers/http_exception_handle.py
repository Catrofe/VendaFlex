from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class HttpExceptionHandler:

    @staticmethod
    def handler(request: Request, exception: HTTPException):
        return JSONResponse(status_code=exception.status_code, content={"message": exception.detail})