import pytest

from x4companion.x4.serializers import SectorSerializerWrite


@pytest.mark.django_db
def test_sector_serializer_write():
    assert SectorSerializerWrite(data={"name": "sector 001"}).is_valid()
