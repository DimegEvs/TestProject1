import pytest


@pytest.mark.asyncio
async def test_create_table(client, created_table):
    response = await client.post("/tables", json={
        "name": "Table 1",
        "seats": 2,
        "location": "У двери"
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "Table with this name already exists"

    response = await client.get("/tables")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data[0]["name"] == "Table 1"
    assert response_data[0]["seats"] == 1
    assert response_data[0]["location"] == "У Окна"


@pytest.mark.asyncio
async def test_delete_table(client, created_table):
    response = await client.delete(f"/tables/{created_table.get('id')}")
    assert response.status_code == 204

    response = await client.delete("/tables/9999")
    assert response.status_code == 404
