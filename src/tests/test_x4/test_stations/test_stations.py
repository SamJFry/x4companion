import pytest


class TestStations:
    @pytest.mark.django_db
    def test_post(self, authed_client):
        pass