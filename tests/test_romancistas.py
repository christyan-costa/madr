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


def test_delecao_romancista(client, token, romancista):
    response = client.delete(
        '/romancista/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado do MADR'}


def test_get_busca_romancista_por_filtro(client, token):
    client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Clarice Lispector'},
    )
    client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Manuel Bandeira'},
    )
    client.post(
        '/romancista',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Paulo Leminski'},
    )

    response = client.get('/romancista/?name=a')

    assert response.status_code == HTTPStatus.OK
    assert response.json() ==     {
        "romancistas": [
            {"name": "clarice lispector", "id": 1},
            {"name": "manuel bandeira", "id": 2},
            {"name": "paulo leminski", "id": 3}
        ]
    }
