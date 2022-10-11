from pydantic import BaseModel

class Student(BaseModel):
    age: int = None
    first_name: str = None
    family_name: str = None
    gender: str = None
    grade: str = None