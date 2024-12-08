import pytest

from x4companion.x4.models import Sector


@pytest.mark.django_db
def test_create_sector(create_basic_sector):
    assert len(Sector.objects.all()) == 1


@pytest.mark.django_db
def test_sector_str(create_basic_sector):
    assert str(create_basic_sector) == "Sector sector 001"
