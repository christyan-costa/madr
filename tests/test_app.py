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


def test_create_user_existing_email(client):
    # First, create a user
    client.post(
        '/conta',
        json={
            'username': 'anotheruser',
            'email': 'existing_email@example.com',
            'password': 'securepassword',
        },
    )

    # Try to create another user with the same username
    response = client.post(
        '/conta',
        json={
            'username': 'existinguser',
            'email': 'existing_email@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}
