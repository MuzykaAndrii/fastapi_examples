from httpx import AsyncClient


async def test_register_user(ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "username": "string",
            "email": "user@example.com",
            "password": "string123",
            "repeat_password": "string123",
        },
    )

    assert response.status_code == 201
