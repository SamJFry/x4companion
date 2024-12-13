import pytest
from django.db import IntegrityError

from x4companion.x4.models import SaveGame, Sector, Station

@pytest.mark.django_db
class TestSector:
    def test_create_sector(self, create_basic_sector):
        assert len(Sector.objects.all()) == 1

    def test_sector_str(self, create_basic_sector):
        assert str(create_basic_sector) == "Sector sector 001"

    def test_sector_unique_names(self, create_basic_sector):
        with pytest.raises(IntegrityError):
            Sector.objects.create(name="sector 001")

@pytest.mark.django_db
class TestSaveGame:
    def test_create_save_game(self, create_save_game):
        assert len(SaveGame.objects.all()) == 1

    def test_save_game_str(self, create_save_game):
        assert str(create_save_game) == "SaveGame Kirk's x4 game"

@pytest.mark.django_db
class TestStation:
    def test_create_stations(self, create_station):
        assert len(Station.objects.all()) == 1

    def test_station_str(self, create_station):
        assert str(create_station) == "Station Hammersmith"
