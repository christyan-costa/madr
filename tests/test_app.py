from http import HTTPStatus


def test_root_deve_retornar_bem_vindo_ao_madr(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Bem-vindo ao Meu Acervo Digital de Romances (MADR)'
    }


def test_create_user_success(client):
    response = client.post(
        '/conta',
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@example.com'

    # Password should not be returned in the response
    assert 'password' not in data


def test_create_user_existing_username(client, user):
    response = client.post(
        '/conta',
        json={
            'username': user.username,
            'email': 'newemail@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


def test_create_user_existing_email(client, user):
    response = client.post(
        '/conta',
        json={
            'username': 'existinguser',
            'email': user.email,
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


def test_update_user_with_wrong_id(client, user, token):
    response = client.put(
        f'/conta/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'another_username',
            'email': 'another@email.com',
            'password': 'another_password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Não autorizado'


def test_update_user_with_correct_id(client, user, token):
    response = client.put(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'another_username',
            'email': 'another@email.com',
            'password': 'another_password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'another_username',
        'email': 'another@email.com',
        'id': user.id,
    }


def test_delete_user_with_wrong_id(client, user, token):
    response = client.delete(
        f'/conta/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Não autorizado'


def test_delete_user_with_correct_id(client, user, token):
    response = client.delete(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_get_token_with_wrong_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong@email.com', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email ou senha incorretos'


def test_get_token_with_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email ou senha incorretos'
