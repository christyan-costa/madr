from http import HTTPStatus


def test_post_criacao_romancista_deve_receber_status_201(client, token):
    response = client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Clarice Lispector'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'clarice lispector'


def test_get_busca_romancista_por_id_deve_receber_status_200(
    client, token, romancista
):
    response = client.get(
        '/romancista/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'clarice lispector'


def test_patch_alteracao_romancista_deve_receber_stataus_200(
    client, token, romancista
):
    response = client.patch(
        '/romancista/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'manuel bandeira'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'manuel bandeira'
