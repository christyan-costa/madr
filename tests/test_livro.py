from http import HTTPStatus


def test_post_livro_deve_receber_status_201_created(client, token):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 1973,
            'title': 'Café Da Manhã Dos Campeões',
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['year'] == 1973  # noqa
    assert response.json()['title'] == 'café da manhã dos campeões'
    assert response.json()['romancista_id'] == 1


def test_patch_alteracao_de_livro(client, token, book_1):
    response = client.patch(
        '/livro/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 1974,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['year'] == 1974  # noqa
    assert response.json()['title'] == 'café da manhã dos campeões'
    assert response.json()['romancista_id'] == 1


def test_get_busca_livro_por_id(client, book_2):
    response = client.get('livro/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['year'] == 1974  # noqa
    assert response.json()['title'] == 'café da manhã dos campeões'
    assert response.json()['romancista_id'] == 1
