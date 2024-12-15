import pytest
from rest_framework import status

from x4companion.x4.models import Station


@pytest.mark.django_db
class TestStations:
    @pytest.mark.usefixtures("_create_multiple_sectors")
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
            {
                "game_id": 1,
                "id": 1,
                "name": "Baron's Court",
                "sector_id": 1,
                "population": 0,
            },
            {
                "game_id": 1,
                "id": 2,
                "name": "Earl's Court",
                "sector_id": 2,
                "population": 0,
            },
        ]

    @pytest.mark.usefixtures("create_station")
    def test_post_cant_create_duplicates(self, authed_client):
        response = authed_client.post(
            "/game/1/stations/",
            {
                "data": [
                    {
                        "name": "Hammersmith",
                        "sector_id": 1,
                    },
                ]
            },
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(Station.objects.all()) == 1

    @pytest.mark.usefixtures("create_station")
    def test_get(self, authed_client):
        response = authed_client.get("/game/1/stations/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "stations": [
                {
                    "game_id": 1,
                    "id": 1,
                    "name": "Hammersmith",
                    "sector_id": 1,
                    "population": 0,
                },
            ]
        }
