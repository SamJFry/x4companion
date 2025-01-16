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
        }

    def test_delete(self, authed_client, create_ware):
        response = authed_client.delete("/dataset/1/wares/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(Ware.objects.all().values()) == []
