from http import HTTPStatus

from tests.conftest import RomancistaFactory


def test_post_livro_deve_receber_status_201_created(client, token, romancista):
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


def test_delete_livro(client, book_1, token):
    response = client.delete(
        '/livro/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado do MADR'}


def test_get_filtro_de_livros(client, token, session):
    # Criando 3 romancistas, para tornar possível a
    # adição de livros com romancista_id variando de
    # 1 a 3 (constraint de foreign key do postgres)
    session.bulk_save_objects(RomancistaFactory.create_batch(3))

    client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 1900,
            'title': 'Café Da Manhã Dos Campeões',
            'romancista_id': 1,
        },
    )

    client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 1900,
            'title': 'Memórias Póstumas de Brás Cubas',
            'romancista_id': 2,
        },
    )

    client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 1865,
            'title': 'Iracema',
            'romancista_id': 3,
        },
    )

    response = client.get('/livro/?title=a&year=1900')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'year': 1900,
                'title': 'café da manhã dos campeões',
                'romancista_id': 1,
                'id': 1,
            },
            {
                'year': 1900,
                'title': 'memórias póstumas de brás cubas',
                'romancista_id': 2,
                'id': 2,
            },
        ]
    }
