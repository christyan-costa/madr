from http import HTTPStatus


def test_post_criacao_romancista(client, token):
    response = client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Clarice Lispector'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'clarice lispector'
