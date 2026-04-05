import json

import pytest
from rest_framework import status

from x4companion.x4.models import Ware


@pytest.mark.django_db
class TestWares:
    def test_post(self, authed_client, create_dataset):
        response = authed_client.post(
            "/dataset/1/wares/",
            json.dumps(
                {
                    "data": [
                        {
                            "name": "Self Sealing Stem Bolts",
                            "storage": "Container",
                            "volume": 1,
                        }
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Ware.objects.all().values()) == [
            {
                "id": 1,
                "dataset_id": 1,
                "name": "Self Sealing Stem Bolts",
                "storage": "C",
                "volume": 1,
            }
        ]

    def test_get(self, authed_client, create_ware):
        response = authed_client.get("/dataset/1/wares/")
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
                    "name": "Stone",
                    "storage": "Solid",
                    "volume": 1,
                }
            ],
        }


@pytest.mark.django_db
class TestWareView:
    def test_get(self, authed_client, create_ware):
        response = authed_client.get("/dataset/1/wares/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "name": "Stone",
            "storage": "Solid",
            "volume": 1,
        }

    def test_delete(self, authed_client, create_ware):
        response = authed_client.delete("/dataset/1/wares/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(Ware.objects.all().values()) == []

    def test_get_ware_metrics(
        self, authed_client, create_factory, create_factory_2, create_user_2_factory
    ):
        response = authed_client.get("/game/1/wares/1/metrics/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "name": "Stone",
            "hourly_products": 7000,
            "hourly_consumption": 0,
            "hourly_energy": 25200,
            "net_products": 0,
        }

    def test_get_ware_metrics_with_consumption(self, authed_client, create_factory, create_consuming_factory):
        response = authed_client.get("/game/1/wares/1/metrics/")
        assert response.json() == {
            "name": "Stone",
            "hourly_products": 5000,
            "hourly_consumption": 1500,
            "hourly_energy": 18000,
            "net_products": 3500,
        }
