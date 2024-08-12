from http import HTTPStatus


def test_root_deve_retornar_bem_vindo_ao_madr(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Bem-vindo ao Meu Acervo Digital de Romances (MADR)'
    }
