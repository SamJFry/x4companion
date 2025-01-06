import json

import pytest
from rest_framework import status

from x4companion.x4.models import SectorTemplate


@pytest.mark.django_db
class TestSectorTemplates:
    def test_post(self, authed_client, create_dataset):
        response = authed_client.post(
            "/dataset/1/sector-templates/",
            json.dumps(
                {
                    "data": [
                        {
                            "name": "sector1",
                            "dataset_id": 1,
                            "sunlight_percent": 100,
                        }
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(SectorTemplate.objects.all().values()) == [
            {
                "id": 1,
                "name": "sector1",
                "dataset_id": 1,
                "sunlight_percent": 100,
            }
        ]

    def test_get(self, authed_client, create_sector_template):
        response = authed_client.get("/dataset/1/sector-templates/")
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
                    "name": "sector 001",
                    "sunlight_percent": 100,
                    "dataset_id": 1,
                }
            ],
        }


@pytest.mark.django_db
class TestSectorTemplatesView:
    def test_get(self, authed_client, create_sector_template):
        response = authed_client.get("/dataset/1/sector-templates/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "name": "sector 001",
            "sunlight_percent": 100,
            "dataset_id": 1,
        }

    def test_delete(self, authed_client, create_sector_template):
        response = authed_client.delete("/dataset/1/sector-templates/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(SectorTemplate.objects.all().values()) == []
