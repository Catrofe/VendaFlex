from fastapi import FastAPI, HTTPException
from .exception_handler import ExceptionHandler
from .http_exception_handle import HttpExceptionHandler

def register_handlers(app: FastAPI):
    app.add_exception_handler(Exception, ExceptionHandler.handler)
    app.add_exception_handler(HTTPException, HttpExceptionHandler.handler)
