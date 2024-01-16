from fastapi import Request
from fastapi.responses import JSONResponse


class ExceptionHandler:

    @staticmethod
    def handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )
