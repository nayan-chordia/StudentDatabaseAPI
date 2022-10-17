from fastapi import Request, status
from fastapi.responses import JSONResponse

class HTTPExceptionHandler(Exception):
    def __init__(self, id:str):
        self.id = id

def http_exception_handler(request: Request, exc: HTTPExceptionHandler):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content = {"detail":f"student with {exc.id} was not found"},
    )