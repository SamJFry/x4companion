import pytest

from x4companion.x4.models import Sector


@pytest.fixture
def create_basic_sector():
    sector = Sector.objects.create(name="sector 001")
    sector.save()
    return sector


@pytest.fixture
def _create_multiple_sectors():
    Sector.objects.bulk_create([Sector(name=f"sector{x}") for x in range(4)])
