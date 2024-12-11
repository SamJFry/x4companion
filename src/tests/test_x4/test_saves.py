import pytest
from rest_framework import status


class TestSaveGameView:
    @pytest.mark.django_db
    def test_post(self, logged_in_client):
        response = logged_in_client.post(
            "/game/",
            {"name": "Spock's Game"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"game_id": 1, "name": "Spock's Game", "user_id": 1}
