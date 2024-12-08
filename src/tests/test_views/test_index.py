import pytest
from pytest_django.fixtures import client

from x4companion import __version__


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "X4 Companion App",
        "version": __version__
    }
