from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_get(create_basic_sector, client, django_user_model):
    user = django_user_model.objects.create_user(
        username="test", password="test"
    )
    client.force_login(user)
    response = client.get("/sectors/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"sectors": [{"name": "sector 001"}]}
