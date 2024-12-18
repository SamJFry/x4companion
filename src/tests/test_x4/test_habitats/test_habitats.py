import pytest
from rest_framework import status

from x4companion.x4.models import HabitatModule


@pytest.mark.django_db
class TestHabitatModules:
    def test_post(self, authed_client, create_dataset):
        response = authed_client.post(
            "/dataset/1/habitat-modules/",
            {
                "data": [
                    {
                        "name": "Bajoran small habitat",
                        "capacity": 250,
                        "species": "Bajoran",
                    }
                ]
            },
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(HabitatModule.objects.all().values()) == [
            {
                "id": 1,
                "dataset_id": 1,
                "name": "Bajoran small habitat",
                "capacity": 250,
                "species": "Bajoran",
            }
        ]

    def test_get(self, authed_client, create_habitat_module):
        response = authed_client.get("/dataset/1/habitat-modules/")
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
                    "name": "Borg Large",
                    "capacity": 1000,
                    "species": "borg",
                }
            ],
        }
