import pytest
from django.forms.models import model_to_dict
from rest_framework import status

from x4companion.x4.models import Sector


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
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"sectors": [{"name": "sector 001"}]}

    @pytest.mark.django_db
    def test_post(self, logged_in_client):
        response = logged_in_client.post("/sectors/", {"name": "test sector"})
        assert response.status_code == status.HTTP_201_CREATED
        assert model_to_dict(Sector.objects.get(name="test sector")) == {
            "id": 1,
            "name": "test sector",
        }

    @pytest.mark.django_db
    def test_post_rejects_bad_request(self, logged_in_client):
        response = logged_in_client.post("/sectors/", {"bad": "data"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"name": ["This field is required."]}
