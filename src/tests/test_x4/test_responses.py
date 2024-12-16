import pytest
from rest_framework import status

from x4companion.x4.responses import post_response
from x4companion.x4.serializers import (
    HabitatModuleSerializer,
    SectorSerializerWrite,
)

POST_CASES = [
    (
        {
            "serializer_class": HabitatModuleSerializer,
            "data": [{"name": "test", "capacity": 1, "species": "bob"}],
        },
        status.HTTP_201_CREATED,
        [{"id": 1, "name": "test", "capacity": 1, "species": "bob"}],
    ),
    (
        {
            "serializer_class": SectorSerializerWrite,
            "data": [{"name": "01"}],
            "context": {"game_id": 1},
        },
        status.HTTP_201_CREATED,
        [{"name": "01"}],
    ),
    (
        {
            "serializer_class": SectorSerializerWrite,
            "data": [{"name": "01"}],
            "context": {"game_id": 123},
        },
        status.HTTP_404_NOT_FOUND,
        {"error": "SaveGame matching query does not exist."},
    ),
]


@pytest.mark.django_db
class TestResponses:
    @pytest.mark.parametrize(("kwargs", "status_code", "expected"), POST_CASES)
    def test_post(self, create_save_game, kwargs, status_code, expected):
        response = post_response(**kwargs)
        assert response.status_code == status_code
        assert response.data == expected
