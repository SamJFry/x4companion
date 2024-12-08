import pytest

from x4companion.x4.models import Sector


@pytest.mark.django_db
def test_create_sector():
    sector = Sector.objects.create(name="sector 001")
    sector.save()
    assert len(Sector.objects.all()) == 1


@pytest.mark.django_db
def test_sector_str():
    sector = Sector.objects.create(name="sector 001")
    sector.save()
    assert str(sector) == "Sector sector 001"
