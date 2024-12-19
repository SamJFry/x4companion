import pytest
from rest_framework import status

from x4companion.x4.models import Habitat


@pytest.mark.django_db
class TestStationHabitats:
    def test_post(self, authed_client, create_habitat_module, create_station):
        response = authed_client.post(
            "/game/1/stations/1/habitats/",
            {"data": [{"module_id": 1, "count": 5}]},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Habitat.objects.all().values()) == [
            {
                "id": 1,
                "count": 5,
                "module_id": 1,
                "station_id": 1,
            }
        ]

    def test_get(
        self,
        authed_client,
        create_habitat_module,
        create_station,
        create_habitat,
    ):
        response = authed_client.get("/game/1/stations/1/habitats/")
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
                    "count": 1,
                    "module_id": 1,
                    "station_id": 1,
                }
            ],
        }


@pytest.mark.django_db
class TestStationHabitatsView:
    def test_get(self, authed_client, create_habitat):
        response = authed_client.get("/game/1/stations/1/habitats/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "count": 1,
            "module_id": 1,
            "station_id": 1,
        }

    def test_get_404_on_not_my_station(
        self, authed_client, create_user_2_habitat
    ):
        response = authed_client.get("/game/1/stations/1/habitats/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
