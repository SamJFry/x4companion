import pytest
from rest_framework import status

from x4companion.x4.models import Dataset


@pytest.mark.django_db
class TestDataset:
    def test_post(self, authed_client):
        response = authed_client.post(
            "/dataset/",
            {"data": [{"name": "StarTrekin"}]},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Dataset.objects.all().values()) == [
            {"id": 1, "name": "StarTrekin"}
        ]

    def test_get(self, authed_client, create_dataset):
        response = authed_client.get("/dataset/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "page": 1,
            "pages": 1,
            "page_size": 100,
            "previous": None,
            "next": None,
            "data": [
                {
                    "id": 1,
                    "name": "StarTrekin",
                }
            ],
        }
