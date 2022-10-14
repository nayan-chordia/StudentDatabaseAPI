from fastapi.testclient import TestClient
from source.queries import students_queries
from fastapi import HTTPException
import pytest
from main import app


client = TestClient(app)

def id_cache():
    cache_id = []
    student = students_queries.select_query()
    for i in range(0,len(student)):
        cache_id.append(dict(student[i])['id'])
    return cache_id

no_id = [10000,10001,-1,-2,0,100000]




@pytest.mark.parametrize("details",[
    {"age":"6", "first_name": "Sarvesh","family_name": "Patel", "gender": "M", "grade": "A"},
    {"age":"10", "first_name": "Kanta","family_name": "Soni", "gender": "F", "grade": "B"},
])
def test_create_student(details):
    res = client.post("/students", json=details)
    assert res.status_code == 201
    res = res.json()
    del res['id']
    res['age'] = str(res['age'])
    assert res == details



def test_get_students():
    res = client.get("/students")
    assert res.status_code == 200
    assert type(res.json()) is list


@pytest.mark.parametrize("id", [id for id in id_cache()])
def test_get_student_by_id(id):
    res = client.get("/students/"+str(id))
    assert res.status_code == 200
    assert res.json().get('id') == id


@pytest.mark.parametrize("id", [id for id in no_id])
def test_get_student_by_id_inexistence(id):
    res = client.get("/students/"+str(id))
    assert res.status_code == 404
    assert res.json() == {"detail": "student with " + str(id) +  " was not found"}


@pytest.mark.parametrize("id", [121,122,123,124,125,126,127,128,129])
def test_update_student(id):
    res = client.patch("/students/"+str(id), json={"gender":"F", "grade":"A"})
    assert res.status_code == 200
    assert res.json().get('id') == id
    assert res.json().get('gender') == 'F'
    assert res.json().get('grade') == 'A'


@pytest.mark.parametrize("id", [id for id in no_id])
def test_update_student_inexistence(id):
    res = client.patch("/students/"+str(id), json={"gender":"F"})
    assert res.status_code == 404
    assert res.json() == {"detail": "student with " + str(id) +" was not found"}


@pytest.mark.parametrize("id", [113,115,116,117])
def test_delete_student(id):
    res = client.delete("/students/"+str(id))
    assert res.status_code == 204

@pytest.mark.parametrize("id", [id for id in no_id])
def test_delete_student_inexistence(id):
    res = client.delete("/students/"+str(id))
    assert res.status_code == 404
    assert res.json() == {"detail": "student with " + str(id) +" was not found"}