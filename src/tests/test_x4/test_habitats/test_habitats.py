import pytest
from rest_framework import status

from x4companion.x4.models import HabitatModule


@pytest.mark.django_db
class TestHabitatModules:
    def test_post(self, authed_client):
        response = authed_client.post(
            "/habitat-modules/",
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
                "name": "Bajoran small habitat",
                "capacity": 250,
                "species": "Bajoran",
            }
        ]
