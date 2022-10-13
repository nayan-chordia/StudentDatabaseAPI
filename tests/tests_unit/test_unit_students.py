from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from main import app


client = TestClient(app)

def test_create_student():
    res = client.post("/students", json={"age":"6", "first_name": "Sarvesh","family_name": "Patel",
                                                    "gender": "M",
                                                    "grade": "A"})
    assert res.status_code == 201
    assert type(res.json()) == dict


def test_get_students():
    res = client.get("/students")
    assert res.status_code == 200
    assert type(res.json()) is list


def test_get_student_by_id():
    res = client.get("/students/1")
    assert res.status_code == 200
    assert type(res.json()) is dict


def test_get_student_by_id_inexistence():
    res = client.get("/students/500")
    assert res.status_code == 404
    assert res.json() == {"detail": "student with 500 was not found"}


def test_update_student():
    res = client.patch("/students/1", json={"gender":"F"})
    assert res.status_code == 200
    assert type(res.json()) == dict


def test_update_student_inexistence():
    res = client.patch("/students/500", json={"gender":"F"})
    assert res.status_code == 404
    assert res.json() == {"detail": "student with 500 was not found"}


def test_delete_student():
    res = client.delete("/students/15")
    assert res.status_code == 204


def test_delete_student_inexistence():
    res = client.delete("/students/500")
    assert res.status_code == 404
    assert res.json() == {"detail": "student with 500 was not found"}   