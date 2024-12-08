import pytest

from x4companion.x4.models import Sector


@pytest.fixture
def create_sector():
    sector = Sector.objects.create(name="sector 001")
    sector.save()
    return sector


@pytest.mark.django_db
def test_create_sector(create_sector):
    assert len(Sector.objects.all()) == 1


@pytest.mark.django_db
def test_sector_str(create_sector):
    assert str(create_sector) == "Sector sector 001"
