import pytest

from x4companion.x4.models import Sector


@pytest.fixture
def create_basic_sector():
    sector = Sector.objects.create(name="sector 001")
    sector.save()
    return sector
