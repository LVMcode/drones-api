import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, Medication, db
from configs import dirs, environment


env = environment.get_environment_variables()


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[db.get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_read_medications(session: Session, client: TestClient):
    medication_1 = Medication(
        code="AZ00_5B", image="http://server.com/image_name1.jpg", name="TestMed1", weight=2.5)
    medication_2 = Medication(
        code="TH0045R", image="http://server.com/image_name2.jpg", name="TestMed2", weight=1.2)
    session.add(medication_1)
    session.add(medication_2)
    session.commit()

    response = client.get("/api/v1/medications/")
    data: list[dict] = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["code"] == "AZ00_5B"
    assert data[0]["image"] == "http://server.com/image_name1.jpg"
    assert data[0]["name"] == "TestMed1"
    assert data[0]["weight"] == 2.5
    assert data[1]["code"] == "TH0045R"
    assert data[1]["image"] == "http://server.com/image_name2.jpg"
    assert data[1]["name"] == "TestMed2"
    assert data[1]["weight"] == 1.2


def test_create_medication(client: TestClient):
    files = [
        ('img_file', ('python.jpg', open(
            'tests/static/python.jpg', 'rb'), 'image/jpeg'))
    ]
    payload = {'name': 'TestMed1',
               'weight': '2.5',
               'code': 'AZ00_5B'}

    response = client.post(
        "/api/v1/medications/", data=payload, files=files
    )
    data: dict = response.json()

    filename = data["image"].split("/")[-1]
    file_path = os.path.join(f"{dirs.MEDICATION_IMAGES_PATH}", filename)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    assert response.status_code == 201
    assert data["code"] == "AZ00_5B"
    assert data["image"] == f"{env.IMAGES_SERVER_PROTOCOL}://{env.IMAGES_SERVER}:{env.IMAGES_SERVER_PORT}/{dirs.MEDICATION_IMAGES_PATH}/{filename}"
    assert data["name"] == "TestMed1"
    assert data["weight"] == 2.5
    assert data["id"] is not None


def test_create_medication_invalid_name(client: TestClient):
    files = [
        ('img_file', ('python.jpg', open(
            'tests/static/python.jpg', 'rb'), 'image/jpeg'))
    ]
    payload = {'name': '/TestMed1',
               'weight': '2.5',
               'code': 'AZ00_5B'}

    response = client.post(
        "/api/v1/medications/", data=payload, files=files
    )

    assert response.status_code == 422


def test_create_medication_invalid_code(client: TestClient):
    files = [
        ('img_file', ('python.jpg', open(
            'tests/static/python.jpg', 'rb'), 'image/jpeg'))
    ]
    payload = {'name': 'TestMed1',
               'weight': '2.5',
               'code': 'aZ00_5B'}

    response = client.post(
        "/api/v1/medications/", data=payload, files=files
    )

    assert response.status_code == 422


def test_read_medication(session: Session, client: TestClient):
    medication_1 = Medication(
        code="AZ00_5B", image="http://server.com/image_name1.jpg", name="TestMed1", weight=2.5)
    session.add(medication_1)
    session.commit()

    response = client.get(f"/api/v1/medications/{medication_1.id}")
    data: dict = response.json()

    assert response.status_code == 200
    assert data["code"] == medication_1.code
    assert data["image"] == medication_1.image
    assert data["name"] == medication_1.name
    assert data["weight"] == medication_1.weight
    assert data["id"] == medication_1.id


def test_delete_medication(session: Session, client: TestClient):
    medication_1 = Medication(
        code="AZ00_5B", image="http://server.com/image_name1.jpg", name="TestMed1", weight=2.5)
    session.add(medication_1)
    session.commit()

    response = client.delete(f"/api/v1/medications/{medication_1.id}")

    medication_in_db = session.get(Medication, medication_1.id)
    assert response.status_code == 204
    assert medication_in_db is None


def test_update_medication(session: Session, client: TestClient):
    medication_1 = Medication(
        code="AZ00_5B", image="http://server.com/image_name1.jpg", name="TestMed1", weight=2.5)
    session.add(medication_1)
    session.commit()

    files = [
        ('img_file', ('python.jpg', open(
            'tests/static/python.jpg', 'rb'), 'image/jpeg'))
    ]

    response = client.patch(
        f"/api/v1/medications/{medication_1.id}", files=files)
    data: dict = response.json()

    filename = data["image"].split("/")[-1]
    file_path = os.path.join(f"{dirs.MEDICATION_IMAGES_PATH}", filename)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    assert response.status_code == 200
    assert data["code"] == medication_1.code
    assert data["image"] == f"{env.IMAGES_SERVER_PROTOCOL}://{env.IMAGES_SERVER}:{env.IMAGES_SERVER_PORT}/{dirs.MEDICATION_IMAGES_PATH}/{filename}"
    assert data["name"] == medication_1.name
    assert data["weight"] == medication_1.weight
    assert data["id"] == medication_1.id
