from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from schemas.reservation import ReservationRead


@pytest.mark.asyncio
async def test_create_reservation(client, created_reservation):
    response = await client.post("/reservations", json={
        "customer_name": "Dmitry",
        "table_id": created_reservation["table_id"],
        "reservation_time": created_reservation["reservation_time"],
        "duration_minutes": 5
    })

    assert response.status_code == 409, f"Error: {response.status_code}, {response.json()}"
    assert response.json()["detail"] == "This table is already reserved for this time slot."
    start_time = datetime.fromisoformat(created_reservation["reservation_time"]) + timedelta(minutes=created_reservation["duration_minutes"])
    response = await client.post("/reservations", json={
        "customer_name": "Dmitry",
        "table_id": created_reservation["table_id"],
        "reservation_time": start_time.isoformat(),
        "duration_minutes": 15
    })
    response_data = response.json()
    assert response.status_code == 201, f"Error: {response.status}, {response.json()}"
    assert response_data["customer_name"] == "Dmitry"
    assert response_data["table_id"] == created_reservation["table_id"]
    assert response_data["reservation_time"] == start_time.isoformat()
    assert response_data["duration_minutes"] == 15

    response = await client.get("/reservations")
    assert response.status_code == 200
    reservations = response.json()
    assert isinstance(reservations, list)
    for _ in reservations:
        try:
            ReservationRead(**response_data)
        except ValidationError as e:
            pytest.fail(f"Response data does not match schema: {e}")


@pytest.mark.asyncio
async def test_delete_reservation(client, created_reservation):
    response = await client.delete(f"/reservations/{created_reservation.get('id')}")
    assert response.status_code == 204

    response = await client.delete(f"/reservations/{created_reservation.get('id')}")
    assert response.status_code == 404

