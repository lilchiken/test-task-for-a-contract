import json
from typing import TYPE_CHECKING

import pytest
from django.contrib.auth.models import User as user_model

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient

TEST_PASSWORD = 'test_pass'


@pytest.fixture
def user_with_password(user: 'User'):
    user.set_password(TEST_PASSWORD)
    user.save()
    return user


@pytest.mark.django_db
def test_auth_using_login_pass(anon_client: 'APIClient', user_with_password: 'User'):
    username = user_with_password.username
    response = anon_client.post(
        '/api/auth/login/',
        data={'username': username, 'password': 'incorrect_password'},
    )
    assert response.status_code == 403

    response = anon_client.post(
        '/api/auth/login/', data={'username': username, 'password': TEST_PASSWORD}
    )
    assert response.status_code == 200, response.content

    data = response.json()

    assert data['username'] == username

# Задание поставило меня в ступор, где было два пути.
# Первый - написать тесты по заданию.
# Второй - написать рабочие тесты исходя из ресурсов проекта.
# Я решил идти по обоим :) Тесты представлены, соответственно списку выше.


@pytest.mark.django_db
def test_user_flow(admin_client: 'APIClient', anon_client: 'APIClient'):
    """Тесты по TODO."""

    valid_username = 'user_{}'
    valid_password = 'password_{}'
    valid_email = 'email_{}@test.task'

    users_count = 10
    valid_users_data = {
        valid_username.format(i): {
            'username': valid_username.format(i),
            'password': valid_password.format(i),
            'email': valid_email.format(i)
        }
        for i in range(1, users_count + 1)
    }

    for valid_user in valid_users_data.values():

        response = admin_client.post('/api/v1/users/', data=valid_user)

        assert response.status_code == 200

    response = admin_client.get('/api/v1/users/')

    assert response.status_code == 200

    users_response_data = response.json()

    assert users_response_data.get('count') == users_count

    users_response_data = users_response_data.get('results')

    for user in users_response_data:

        user_password = valid_users_data[user.get('username')].get('password')

        response = anon_client.post(
            '/api/v1/users/{}/'.format(user.get('id')),
            data={
                'username': user.get('username'),
                'password': user_password
            }
        )
        assert response.status_code == 200, response.content

    for user in users_response_data:

        response = admin_client.delete('/api/v1/users/{}/'.format(user.get('id')))

        assert response.status_code == 204


@pytest.mark.django_db
def test_user_flow_correct(admin_client: 'APIClient', anon_client: 'APIClient'):
    """Тесты по рабочим эндпоинтам."""

    valid_username = 'user_{}'
    valid_password = 'password_{}'
    valid_email = 'email_{}@test.task'

    users_count = 10
    valid_users_data = {
        valid_username.format(i): {
            'username': valid_username.format(i),
            'password': valid_password.format(i),
            'email': valid_email.format(i)
        }
        for i in range(1, users_count + 1)
    }
    users_count_before = user_model.objects.count()

    for valid_user in valid_users_data.values():

        response = admin_client.post('/api/v1/users/', data=valid_user)

        # метод create в UserSerializer не отдаёт статус 200 :)
        assert response.status_code in (200, 201)

    response = admin_client.get('/api/v1/users/')

    assert response.status_code == 200

    users_response_data = response.json()

    users_count_after_create = user_model.objects.count() - users_count_before

    assert users_response_data.get('count') == users_count == users_count_after_create

    users_response_data = users_response_data.get('results')

    for user in users_response_data:

        user_password = valid_users_data[user.get('username')].get('password')

        # 1. Эндпоинт api/v1/users/{user.id} доступен только админу.
        # 2. Этот эндпоинт не настроен на проверку авторизации.
        response = anon_client.post(
            '/api/auth/login/',
            data={
                'username': user.get('username'),
                'password': user_password
            }
        )
        assert response.status_code == 200, response.content

    users_count_before = user_model.objects.count()

    for user in users_response_data:

        response = admin_client.delete('/api/v1/users/{}/'.format(user.get('id')))

        assert response.status_code == 204

    assert user_model.objects.count() == users_count_before - users_count
