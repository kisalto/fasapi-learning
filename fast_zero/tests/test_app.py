from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Joshua',
            'email': 'teste@email.com',
            'password': 'senha',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Joshua',
        'email': 'teste@email.com',
        'id': 1,
    }


def test_update(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Allan',
            'email': 'allan@email.com',
            'password': 'senha',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Allan',
        'email': 'allan@email.com',
        'id': 1,
    }


def test_update_err(client):
    response = client.put(
        '/users/2', json={'username': '', 'email': '', 'password': ''}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_del_err(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT

    assert response_update.json() == {
        'detail': 'Username ou Email ja existe'
    }


# def test_del(client):
#     response = client.delete('/users/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'message': 'User deleted'}
