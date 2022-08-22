import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, Drone, Medication, db
from configs import dirs, environment
from models.drone_model import State, Model


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


def test_read_drones(session: Session, client: TestClient):
    drone_1 = Drone(state=State.IDLE, model=Model.Lightweight,
                    battery_capacity=100, serial_number="DA0144", weight_limit=250)
    drone_2 = Drone(state=State.LOADING, model=Model.Heavyweight,
                    battery_capacity=100, serial_number="DA0144")

    session.add(drone_1)
    session.add(drone_2)
    session.commit()

    response = client.get("/api/v1/drones/")
    data: list[dict] = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["state"] == drone_1.state
    assert data[0]["model"] == drone_1.model
    assert data[0]["battery_capacity"] == drone_1.battery_capacity
    assert data[0]["serial_number"] == drone_1.serial_number
    assert data[0]["weight_limit"] == drone_1.weight_limit
    assert data[0]["id"] == drone_1.id
    assert data[1]["state"] == drone_2.state
    assert data[1]["model"] == drone_2.model
    assert data[1]["battery_capacity"] == drone_2.battery_capacity
    assert data[1]["serial_number"] == drone_2.serial_number
    assert data[1]["weight_limit"] == drone_2.weight_limit
    assert data[1]["id"] == drone_2.id


def test_create_drone(client: TestClient):
    response = client.post(
        "/api/v1/drones/", json={"serial_number": "DA0144",
                                 "model": Model.Middleweight,
                                 "weight_limit": 350,
                                 "battery_capacity": 100,
                                 "state": State.IDLE}
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data["state"] == State.IDLE
    assert data["model"] == Model.Middleweight
    assert data["battery_capacity"] == 100
    assert data["serial_number"] == "DA0144"
    assert data["weight_limit"] == 350
    assert data["id"] is not None


def test_create_drone_invalid_serial_number(client: TestClient):
    invalid_serial_number = "A" * 101
    response = client.post(
        "/api/v1/drones/", json={"serial_number": invalid_serial_number,
                                 "model": Model.Middleweight,
                                 "weight_limit": 500,
                                 "battery_capacity": 100,
                                 "state": State.IDLE}
    )
    data: dict = response.json()

    assert response.status_code == 422


def test_create_drone_invalid_weight_limit(client: TestClient):
    response = client.post(
        "/api/v1/drones/", json={"serial_number": "DA0144",
                                 "model": Model.Middleweight,
                                 "weight_limit": 501,
                                 "battery_capacity": 100,
                                 "state": State.IDLE}
    )
    data: dict = response.json()

    assert response.status_code == 422


def test_create_drone_invalid_battery_capacity(client: TestClient):
    response = client.post(
        "/api/v1/drones/", json={"serial_number": "DA0144",
                                 "model": Model.Middleweight,
                                 "weight_limit": 500,
                                 "battery_capacity": 130,
                                 "state": State.IDLE}
    )
    data: dict = response.json()

    assert response.status_code == 422


def test_available_for_loading(session: Session, client: TestClient):
    drone_1 = Drone(state=State.IDLE, model=Model.Lightweight,
                    battery_capacity=100, serial_number="DA0144", weight_limit=250)
    drone_2 = Drone(state=State.LOADING, model=Model.Heavyweight,
                    battery_capacity=100, serial_number="DA0144")

    session.add(drone_1)
    session.add(drone_2)
    session.commit()

    response = client.get("/api/v1/drones/availableForLoading")
    data: list[dict] = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["state"] == drone_1.state
    assert data[0]["model"] == drone_1.model
    assert data[0]["battery_capacity"] == drone_1.battery_capacity
    assert data[0]["serial_number"] == drone_1.serial_number
    assert data[0]["weight_limit"] == drone_1.weight_limit
    assert data[0]["id"] == drone_1.id


def test_read_drone(session: Session, client: TestClient):
    drone_1 = Drone(state=State.IDLE, model=Model.Lightweight,
                    battery_capacity=100, serial_number="DA0144", weight_limit=250)

    session.add(drone_1)
    session.commit()

    response = client.get(f"/api/v1/drones/{drone_1.id}")
    data: dict = response.json()

    assert response.status_code == 200
    assert data["state"] == drone_1.state
    assert data["model"] == drone_1.model
    assert data["battery_capacity"] == drone_1.battery_capacity
    assert data["serial_number"] == drone_1.serial_number
    assert data["weight_limit"] == drone_1.weight_limit
    assert data["id"] == drone_1.id


def test_delete_drone(session: Session, client: TestClient):
    drone_1 = Drone(state=State.IDLE, model=Model.Lightweight,
                    battery_capacity=100, serial_number="DA0144", weight_limit=250)
    session.add(drone_1)
    session.commit()

    response = client.delete(f"/api/v1/drones/{drone_1.id}")

    medication_in_db = session.get(Drone, drone_1.id)
    assert response.status_code == 204
    assert medication_in_db is None


def test_update_drone(session: Session, client: TestClient):
    drone_1 = Drone(state=State.IDLE, model=Model.Lightweight,
                    battery_capacity=100, serial_number="DA0144", weight_limit=100)
    medication_1 = Medication(
        code="AZ00_5B", image="http://server.com/image_name1.jpg", name="TestMed1", weight=40)
    medication_2 = Medication(
        code="TH0045R", image="http://server.com/image_name2.jpg", name="TestMed2", weight=60)
    session.add(drone_1)
    session.add(medication_1)
    session.add(medication_2)
    session.commit()

    response = client.patch(
        f"/api/v1/drones/{drone_1.id}", json={"battery_capacity": 100,
                                              "state": State.IDLE,
                                              "medication_ids": [medication_1.id, medication_2.id]}
    )
    data: dict = response.json()

    assert response.status_code == 200
    assert data["state"] == drone_1.state
    assert data["model"] == drone_1.model
    assert data["battery_capacity"] == drone_1.battery_capacity
    assert data["serial_number"] == drone_1.serial_number
    assert data["weight_limit"] == drone_1.weight_limit
    assert data["id"] == drone_1.id


def test_update_drone_invalid_medication_weight(session: Session, client: TestClient):
    drone_1 = Drone(state=State.IDLE, model=Model.Lightweight,
                    battery_capacity=100, serial_number="DA0144", weight_limit=100)
    medication_1 = Medication(
        code="AZ00_5B", image="http://server.com/image_name1.jpg", name="TestMed1", weight=40)
    medication_2 = Medication(
        code="TH0045R", image="http://server.com/image_name2.jpg", name="TestMed2", weight=70)
    session.add(drone_1)
    session.add(medication_1)
    session.add(medication_2)
    session.commit()

    response = client.patch(
        f"/api/v1/drones/{drone_1.id}", json={
            "medication_ids": [medication_1.id, medication_2.id]}
    )

    assert response.status_code == 400
