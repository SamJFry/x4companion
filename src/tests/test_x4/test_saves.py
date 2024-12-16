import pytest
from rest_framework import status

from x4companion.x4.models import SaveGame


@pytest.mark.django_db
class TestSaveGames:
    def test_post(self, authed_client):
        response = authed_client.post(
            "/game/",
            {"name": "Spock's Game"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"id": 1, "name": "Spock's Game", "user": 1}

    @pytest.mark.usefixtures("_create_multiple_saves")
    def test_get(self, authed_client):
        response = authed_client.get("/game/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "data": [
                {"id": 1, "name": "game_0", "user": 1},
                {"id": 2, "name": "game_1", "user": 1},
                {"id": 3, "name": "game_2", "user": 1},
            ]
        }


@pytest.mark.django_db
class TestSaveGameView:
    @pytest.mark.usefixtures("_create_multiple_saves")
    @pytest.mark.parametrize(("id_", "expected"), [(1, 200), (123, 404)])
    def test_get(self, authed_client, id_, expected):
        response = authed_client.get(f"/game/{id_}/")
        assert response.status_code == expected
        if response == status.HTTP_200_OK:
            assert response.json() == {"id": 1, "name": "game_0", "user": 1}

    @pytest.mark.usefixtures("_create_multiple_saves")
    def test_delete(self, authed_client):
        response = authed_client.delete("/game/2/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(SaveGame.objects.all().values()) == [
            {"id": 1, "name": "game_0", "user_id": 1},
            {"id": 3, "name": "game_2", "user_id": 1},
        ]

    @pytest.mark.usefixtures("_create_multiple_saves")
    @pytest.mark.parametrize("id_", [1, 123])
    def test_delete_not_exist(self, authed_client_2, id_):
        response = authed_client_2.delete(f"/game/{id_}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
