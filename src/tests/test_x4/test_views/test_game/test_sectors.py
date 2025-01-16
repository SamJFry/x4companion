import json

import pytest
from rest_framework import status

from x4companion.x4.models import Sector


@pytest.mark.django_db
class TestSectors:
    def test_get(self, create_basic_sector, authed_client):
        response = authed_client.get("/game/1/sectors/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "page": 1,
            "pages": 1,
            "page_size": 100,
            "previous": None,
            "next": None,
            "data": [{"id": 1, "game_id": 1, "template_id": 1}],
        }

    def test_get_on_bad_game_gives_404(self, authed_client):
        response = authed_client.get("/game/100/sectors/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.usefixtures("_create_multiple_sector_templates")
    def test_post(self, authed_client, create_save_game):
        response = authed_client.post(
            "/game/1/sectors/",
            json.dumps(
                {
                    "data": [
                        {"template_id": 1},
                        {"template_id": 2},
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Sector.objects.all().values()) == [
            {"game_id": 1, "id": 1, "template_id": 1},
            {"game_id": 1, "id": 2, "template_id": 2},
        ]

    def test_post_rejects_bad_request(self, authed_client):
        response = authed_client.post("/game/1/sectors/", {"bad": "data"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"non_field_errors": ["No data provided"]}


@pytest.mark.django_db
class TestSectorView:
    def test_get(self, create_basic_sector, authed_client):
        response = authed_client.get("/game/1/sectors/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": 1, "game_id": 1, "template_id": 1}

    def test_get_does_not_give_others_sectors(
        self, create_basic_sector, create_user_2_save_game, authed_client_2
    ):
        response = authed_client_2.get("/game/2/sectors/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_does_not_exist(self, authed_client):
        response = authed_client.get("/game/1/sectors/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.usefixtures("_create_multiple_sectors")
    def test_delete(self, authed_client):
        response = authed_client.delete("/game/1/sectors/2/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(Sector.objects.all().values()) == [
            {"game_id": 1, "id": 1, "template_id": 1},
            {"game_id": 1, "id": 3, "template_id": 3},
            {"game_id": 1, "id": 4, "template_id": 4},
        ]

    def test_cant_delete_others_sectors(
        self, create_basic_sector, create_user_2_save_game, authed_client_2
    ):
        response = authed_client_2.delete("/game/2/sectors/1/")
        assert list(Sector.objects.filter(id=1).values()) == [
            {"id": 1, "template_id": 1, "game_id": 1}
        ]
        assert response.status_code == status.HTTP_404_NOT_FOUND
