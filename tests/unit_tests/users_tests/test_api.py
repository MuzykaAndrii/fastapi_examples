import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "username, email, password, repeat_password, response_status",
    [
        (
            "somename",
            "someemail@example.com",
            "somepassword",
            "somepassword",
            201,
        ),
        (
            "somename",
            "someemail@example.com",
            "somepassword",
            "somepassword",
            409,
        ),
        (
            "somename1",
            "someemail1@example.com",
            "somepassword1",
            "somepassword",
            422,
        ),
        (
            "somename2",
            "someemailexample.com",
            "somepassword",
            "somepassword",
            422,
        ),
        (
            "",
            "someemail1@example.com",
            "somepassword",
            "somepassword",
            422,
        ),
        (
            "somename1",
            "someemail1@example.com",
            "some",
            "some",
            422,
        ),
        (
            "somename1",
            "someemail1@example.com",
            "somepassword",
            "some",
            422,
        ),
        (
            "somename1",
            "",
            "somepassword",
            "somepassword",
            422,
        ),
    ],
)
async def test_register_user(
    username, email, password, repeat_password, response_status, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "repeat_password": repeat_password,
        },
    )

    assert response.status_code == response_status


@pytest.mark.parametrize(
    "username_or_email, password, response_status",
    [
        ("testuser1", "testpassword", 200),
        ("testuser1@gmail.cpm", "testpassword", 200),
        ("testuser2@gmail.cpm", "testpassword", 200),
        ("testuser3", "testpassword", 200),
        ("testuser2", "testpassword", 200),
        ("fake@gmail.cpm", "testpassword", 401),
        ("testuser1@gmail.cpm", "wrongpass", 401),
        ("testuser1gmail.cpm", "testpassword", 401),
        ("", "testpassword", 422),
        ("testuser1@gmail.cpm", "", 422),
    ],
)
async def test_login_user(
    username_or_email, password, response_status, ac: AsyncClient
):
    response = await ac.post(
        "/auth/login",
        json={
            "username_or_email": username_or_email,
            "password": password,
        },
    )

    assert response.status_code == response_status
