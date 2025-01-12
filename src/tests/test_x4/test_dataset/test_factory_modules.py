import json

import pytest
from rest_framework import status

from x4companion.x4.models import FactoryModule


@pytest.mark.django_db
class TestHabitatModules:
    def test_post(self, authed_client, create_ware):
        response = authed_client.post(
            "/dataset/1/factory-modules/",
            json.dumps(
                {
                    "data": [
                        {
                            "name": "Stone Factory",
                            "ware_id": 1,
                            "hourly_production": 3600,
                            "hourly_energy": 3600,
                            "workforce": 1000,
                        }
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(FactoryModule.objects.all().values()) == [
            {
                "id": 1,
                "name": "Stone Factory",
                "dataset_id": 1,
                "ware_id": 1,
                "hourly_production": 3600,
                "hourly_energy": 3600,
                "workforce": 1000,
            }
        ]

    def test_get(self, authed_client, create_ware):
        response = authed_client.get("/dataset/1/factory-modules/")
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
                    "name": "Stone Factory",
                    "dataset_id": 1,
                    "ware_id": 1,
                    "hourly_production": 1000,
                    "hourly_energy": 3600,
                    "workforce": 1000,
                }
            ],
        }


@pytest.mark.django_db
class TestHabitatModulesView:
    def test_get(self, authed_client, create_habitat_module):
        response = authed_client.get("/dataset/1/factory-modules/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "name": "Stone Factory",
            "dataset_id": 1,
            "ware_id": 1,
            "hourly_production": 1000,
            "hourly_energy": 3600,
            "workforce": 1000,
        }

    def test_delete(self, authed_client, create_habitat_module):
        response = authed_client.delete("/dataset/1/factory-modules/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(FactoryModule.objects.all().values()) == []
