from fastapi import FastAPI
from source.apis import students_api

app = FastAPI()

app.include_router(students_api.router)
