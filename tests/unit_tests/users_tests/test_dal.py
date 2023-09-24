import pytest
from sqlalchemy.exc import InvalidRequestError

from src.users.dal import UserDAL
from src.users.exceptions import (
    EmailAlreadyInUseError,
    UsernameAlreadyInUseError,
)


@pytest.mark.parametrize(
    "id, username, email, exists",
    [
        (1, "testuser1", "testuser1@gmail.com", True),
        (2, "testuser2", "testuser2@gmail.com", True),
        (3, "testuser3", "testuser3@gmail.com", True),
        (0, "testuser1", "testuser1@gmail.com", False),
        (-1, "testuser1", "testuser1@gmail.com", False),
    ],
)
async def test_get_user_by_id_dal(id, username, email, exists):
    user = await UserDAL.get_by_id(id)

    if exists:
        assert user
        assert user.username == username
        assert user.email == email
        assert user.id == id
    else:
        assert not user


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("newuser1", "newuser1@mail.com", "testpassword"),
        ("newuser2", "newuser2@mail.com", "testpassword"),
        ("newuser3", "newuser3@mail.com", "testpassword"),
    ],
)
async def test_create_user_dal(username, email, password):
    created_user = await UserDAL.create(
        username=username,
        email=email,
        hashed_password=password,
    )

    assert created_user.username == username
    assert created_user.email == email
    assert created_user.hashed_password == password


@pytest.mark.parametrize(
    "username_or_email, expected_user_id",
    [
        ("testuser1@gmail.com", 1),
        ("testuser2@gmail.com", 2),
        ("testuser3@gmail.com", 3),
        ("nonexistent@gmail.com", None),
        ("testuser1", 1),
        ("testuser2", 2),
        ("testuser3", 3),
        ("nonexistent", None),
    ],
)
async def test_get_user_by_email_or_username(username_or_email, expected_user_id):
    found_user = await UserDAL.get_user_by_email_or_username(username_or_email)

    if not expected_user_id:
        assert found_user == None
    else:
        assert found_user != None
        assert found_user.id == expected_user_id


@pytest.mark.parametrize(
    "email_or_username, expected_exception",
    [
        ("testuser1@gmail.com", EmailAlreadyInUseError),
        ("testuser2@gmail.com", EmailAlreadyInUseError),
        ("testuser3@gmail.com", EmailAlreadyInUseError),
        ("nonexistent@gmail.com", None),
        ("testuser1", UsernameAlreadyInUseError),
        ("testuser2", UsernameAlreadyInUseError),
        ("testuser3", UsernameAlreadyInUseError),
        ("nonexistent", None),
    ],
)
async def test_check_email_or_username_existence(email_or_username, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            await UserDAL.check_email_or_username_existence(
                email_or_username, email_or_username
            )
    else:
        await UserDAL.check_email_or_username_existence(
            email_or_username, email_or_username
        )


@pytest.mark.parametrize(
    "filter_criteria, expected_result",
    [
        ({"email": "testuser1@gmail.com"}, True),
        ({"email": "nonexistent@gmail.com"}, False),
        ({"username": "testuser1"}, True),
        ({"username": "nonexistent"}, False),
        ({"id": 1}, True),
        ({"id": 100}, False),
        ({"role_id": 1}, True),
        ({"role_id": 100}, False),
    ],
)
async def test_exists_by(filter_criteria, expected_result):
    result = await UserDAL.exists_by(**filter_criteria)
    assert result == expected_result


@pytest.mark.parametrize(
    "filter_criteria, expected_exception",
    [
        ({"email": "testuser1@gmail.com"}, None),
        ({"absent": "..."}, InvalidRequestError),
        ({"": ""}, InvalidRequestError),
    ],
)
async def test_exists_by_with_exception(filter_criteria, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            await UserDAL.exists_by(**filter_criteria)
    else:
        await UserDAL.exists_by(**filter_criteria)
