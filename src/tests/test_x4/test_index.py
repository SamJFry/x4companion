from http import HTTPStatus

from x4companion import __version__


def test_index(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "name": "X4 Companion App",
        "version": __version__,
    }
