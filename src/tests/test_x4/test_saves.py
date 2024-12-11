import pytest
from rest_framework import status

from tests.conftest import logged_in_client


class TestSaveGameView:
    @pytest.mark.django_db
    def test_post(self, logged_in_client):
        response = logged_in_client.post(
            "/game/",
            {"name": "Spock's Game"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"id": 1, "name": "Spock's Game", "user": 1}

    @pytest.mark.django_db
    def test_get(self, _create_multiple_saves, logged_in_client):
        response = logged_in_client.get("/game/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "saves": [
                {"id": 1, "name": "game_0", "user": 1},
                {"id": 2, "name": "game_1", "user": 1},
                {"id": 3, "name": "game_2", "user": 1},
            ]
        }