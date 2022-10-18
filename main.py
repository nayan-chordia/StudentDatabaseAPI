from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from source.apis import students_api
from source.exceptions import apis_exceptions, service_exceptions

app = FastAPI()

app.add_exception_handler(RequestValidationError, apis_exceptions.validation_exception_handler)
app.add_exception_handler(service_exceptions.HTTPExceptionHandler, service_exceptions.http_exception_handler)
app.include_router(students_api.router)