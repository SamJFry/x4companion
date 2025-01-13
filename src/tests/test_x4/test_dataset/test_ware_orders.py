import json

import pytest
from rest_framework import status

from x4companion.x4.models import WareOrder


@pytest.mark.django_db
class TestWareOrders:
    def test_post(self, authed_client, create_factory_module):
        response = authed_client.post(
            "/dataset/1/ware-orders/",
            json.dumps(
                {
                    "data": [
                        {
                            "ware_id": 1,
                            "factory_module_id": 1,
                            "quantity": 3600,
                        }
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(WareOrder.objects.all().values()) == [
            {
                "id": 1,
                "ware_id": 1,
                "factory_module_id": 1,
                "quantity": 3600,
            }
        ]

    def test_get(self, authed_client, create_ware_order):
        response = authed_client.get("/dataset/1/ware-orders/")
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
                    "ware_id": 1,
                    "factory_module_id": 1,
                    "quantity": 400,
                }
            ],
        }

