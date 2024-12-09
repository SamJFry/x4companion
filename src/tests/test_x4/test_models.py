import pytest

from django.db import IntegrityError

from x4companion.x4.models import Sector

class TestSector:
    @pytest.mark.django_db
    def test_create_sector(self, create_basic_sector):
        assert len(Sector.objects.all()) == 1

    @pytest.mark.django_db
    def test_sector_str(self, create_basic_sector):
        assert str(create_basic_sector) == "Sector sector 001"

    @pytest.mark.django_db
    def test_sector_unique_names(self, create_basic_sector):
        with pytest.raises(IntegrityError):
            Sector.objects.create(name="sector 001")
