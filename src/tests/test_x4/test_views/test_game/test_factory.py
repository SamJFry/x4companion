import json

import pytest
from rest_framework import status

from x4companion.x4.models import Factory


@pytest.mark.django_db
class TestStationFactories:
    def test_post(self, authed_client, create_factory_module, create_station):
        response = authed_client.post(
            "/game/1/stations/1/factories/",
            json.dumps({"data": [{"module_id": 1, "count": 5}]}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Factory.objects.all().values()) == [
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
        create_factory_module,
        create_station,
        create_factory,
    ):
        response = authed_client.get("/game/1/stations/1/factories/")
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
                    "count": 5,
                    "module_id": 1,
                    "station_id": 1,
                }
            ],
        }


@pytest.mark.django_db
class TestStationFactoriesView:
    def test_get(self, authed_client, create_factory):
        response = authed_client.get("/game/1/stations/1/factories/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "count": 5,
            "module_id": 1,
            "station_id": 1,
        }

    def test_get_404_on_not_my_station(
        self,
        authed_client,
        create_user_2_factory,
    ):
        response = authed_client.get("/game/1/stations/1/factories/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete(self, authed_client, create_factory):
        response = authed_client.delete("/game/1/stations/1/factories/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_404_on_not_my_station(
        self, authed_client, create_user_2_factory
    ):
        response = authed_client.delete("/game/1/stations/1/factories/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
