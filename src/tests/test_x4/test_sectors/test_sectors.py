import pytest
from django.contrib.auth.models import User
from rest_framework import status

from x4companion.x4.models import Sector


class TestSectors:
    @pytest.mark.django_db
    def test_get(self, create_basic_sector, logged_in_client):
        response = logged_in_client.get("/game/1/sectors/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "sectors": [{"game_id": 1, "name": "sector 001"}]
        }

    @pytest.mark.django_db
    def test_post(self, logged_in_client, create_save_game):
        response = logged_in_client.post(
            "/game/1/sectors/",
            {
                "data": [
                    {"name": "test sector"},
                    {"name": "cool sector"},
                ]
            },
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert list(Sector.objects.all().values()) == [
            {"game_id": 1, "id": 1, "name": "test sector"},
            {"game_id": 1, "id": 2, "name": "cool sector"},
        ]

    @pytest.mark.django_db
    def test_post_rejects_bad_request(self, logged_in_client):
        response = logged_in_client.post("/game/1/sectors/", {"bad": "data"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"non_field_errors": ["No data provided"]}


class TestSectorView:
    @pytest.mark.django_db
    def test_get(self, create_basic_sector, logged_in_client):
        response = logged_in_client.get("/game/1/sectors/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"game_id": 1, "name": "sector 001"}

    @pytest.mark.django_db
    @pytest.mark.usefixtures("create_basic_sector")
    def test_get_does_not_give_others_sectors(
        self, create_basic_sector, create_user_2_save_game, client
    ):
        user = User.objects.get(id=2)
        client.force_login(user)
        response = client.get("/game/2/sectors/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_does_not_exist(self, logged_in_client):
        response = logged_in_client.get("/game/1/sectors/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    @pytest.mark.usefixtures("_create_multiple_sectors")
    def test_delete(self, logged_in_client):
        response = logged_in_client.delete("/game/1/sectors/2/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(Sector.objects.all().values()) == [
            {"game_id": 1, "id": 1, "name": "sector0"},
            {"game_id": 1, "id": 3, "name": "sector2"},
            {"game_id": 1, "id": 4, "name": "sector3"},
        ]

    @pytest.mark.django_db
    def test_cant_delete_others_sectors(
        self, create_basic_sector, create_user_2_save_game, client
    ):
        user = User.objects.get(id=2)
        client.force_login(user)
        response = client.delete("/game/2/sectors/1/")
        assert list(Sector.objects.filter(id=1).values()) == [
            {"id": 1, "name": "sector 001", "game_id": 1}
        ]
        assert response.status_code == status.HTTP_404_NOT_FOUND
