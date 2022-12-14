from typing import Literal

import pytest
from httpx import AsyncClient
from jose import jwt

from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM
from backend.src.config import DEFAULT_API_PREFIX
from backend.src.tests.conftest import PRELOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_login_for_access_token(client: AsyncClient):
    login_data = {
        "username": "testmail@example.com",
        "password": "test_password"
    }

    response = await client.post(f'{DEFAULT_API_PREFIX}/token/', data=login_data)
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'

    jwt_token = response.json()['access_token']
    jwt_token_decoded = jwt.decode(jwt_token, JWT_SECRET_KEY, JWT_ALGORITHM)
    assert jwt_token_decoded['sub'] == login_data['username']


async def test_login_for_access_token_wrong_data(client: AsyncClient):
    login_data = {}
    response = await client.post(f'{DEFAULT_API_PREFIX}/token/', data=login_data)
    assert response.status_code == 422

    login_data = {"username": "test"}
    response = await client.post(f'{DEFAULT_API_PREFIX}/token/', data=login_data)
    assert response.status_code == 422

    login_data = {
        "username": "testmail@example.com",
        "password": "wrongpass"
    }
    response = await client.post(f'{DEFAULT_API_PREFIX}/token/', data=login_data)
    assert response.status_code == 401
    assert response.json()['detail'] == 'Incorrect email or password'


async def test_get_current_user(client: AsyncClient, auth_headers_superuser: tuple[Literal["Authorization"], str]):
    response = await client.get(f'{DEFAULT_API_PREFIX}/users/me/', headers=[auth_headers_superuser])
    assert response.status_code == 200
    response_user_data = response.json()
    preload_user_data = PRELOAD_DATA['user_1']
    assert len(response_user_data) == 5
    assert response_user_data['email'] == preload_user_data['data']['email']
    assert response_user_data['is_superuser'] == preload_user_data['data']['is_superuser']
    assert response_user_data['is_active'] is True


async def test_get_current_user_wrong_data(client: AsyncClient):
    response = await client.get(f'{DEFAULT_API_PREFIX}/users/me/')
    assert response.status_code == 401

    response = await client.get(f'{DEFAULT_API_PREFIX}/users/me/', headers=[("Authorization", "test")])
    assert response.status_code == 401


async def test_get_certain_user(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        auth_headers_ordinary_user: tuple[Literal["Authorization"], str]
):
    response = await client.get(f'{DEFAULT_API_PREFIX}/users/2/', headers=[auth_headers_superuser])
    assert response.status_code == 200
    response_user_data = response.json()
    preload_user_data = PRELOAD_DATA['user_2']
    assert len(response_user_data) == 5
    assert response_user_data['id'] == 2
    assert response_user_data['email'] == preload_user_data['data']['email']
    assert response_user_data['is_superuser'] == preload_user_data['data']['is_superuser']
    assert response_user_data['is_active'] is True

    response = await client.get(f'{DEFAULT_API_PREFIX}/users/2/', headers=[auth_headers_ordinary_user])
    assert response.status_code == 200
    response_user_data = response.json()
    assert len(response_user_data) == 5
    assert response_user_data['id'] == 2


async def test_get_certain_user_wrong_data(
        client: AsyncClient,
        auth_headers_superuser: tuple[Literal["Authorization"], str],
        auth_headers_ordinary_user: tuple[Literal["Authorization"], str]
):
    response = await client.get(f'{DEFAULT_API_PREFIX}/users/1/', headers=[auth_headers_ordinary_user])
    assert response.status_code == 403

    response = await client.get(f'{DEFAULT_API_PREFIX}/users/1/')
    assert response.status_code == 401

    response = await client.get(f'{DEFAULT_API_PREFIX}/users/1/', headers=[('Authorization', 'test')])
    assert response.status_code == 401

    response = await client.get(f'{DEFAULT_API_PREFIX}/users/999/', headers=[auth_headers_superuser])
    assert response.status_code == 404

    response = await client.get(f'{DEFAULT_API_PREFIX}/users/test/', headers=[auth_headers_superuser])
    assert response.status_code == 422


async def test_create_user(
        client: AsyncClient,
):
    user_data = {
        "email": "test123@example.com",
        "password1": "test_password",
        "password2": "test_password",
    }
    response = await client.post(
        f'{DEFAULT_API_PREFIX}/users/',
        json=user_data,
    )
    response_user_data = response.json()
    assert len(response_user_data) == 5
    assert response_user_data['email'] == user_data['email']
    assert response_user_data['is_active'] is True
    assert response_user_data['is_superuser'] is False

# TODO make test_create_user_wrong_data
