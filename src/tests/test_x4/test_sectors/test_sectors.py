from http import HTTPStatus

import pytest


@pytest.fixture
def logged_in_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="test", password="test"
    )
    client.force_login(user)
    return client


class TestSectors:
    @pytest.mark.django_db
    def test_get(self, create_basic_sector, logged_in_client):
        response = logged_in_client.get("/sectors/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"sectors": [{"name": "sector 001"}]}

    @pytest.mark.django_db
    def test_post(self, logged_in_client):
        response = logged_in_client.post("/sectors/", {"name": "test sector"})
        assert response.status_code == HTTPStatus.CREATED
