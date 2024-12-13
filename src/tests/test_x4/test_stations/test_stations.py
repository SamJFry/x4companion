import pytest
from rest_framework import status

from x4companion.x4.models import Station


@pytest.mark.django_db
@pytest.mark.usefixtures("_create_multiple_sectors")
class TestStations:
    def test_post(self, authed_client):
        response = authed_client.post(
            "/game/1/stations/",
            {
                "data": [
                    {
                        "name": "Baron's Court",
                        "sector_id": 1,
                    },
                    {
                        "name": "Earl's Court",
                        "sector_id": 2,
                    },
                ]
            },
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Station.objects.all().values()) == [
            {"game_id": 1, "name": "Baron's Court", "sector_id": 1, "population": 0},
            {"game_id": 1, "name": "Earl's Court", "sector_id": 2, "population": 0}
        ]