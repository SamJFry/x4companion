import pytest

from x4companion.x4.serializers import SectorSerializer


@pytest.mark.django_db
def test_sector_serializer():
    assert SectorSerializer(data={"name": "sector 001"}).is_valid()
