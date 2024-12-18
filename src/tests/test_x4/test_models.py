import pytest
from django.db import IntegrityError

from x4companion.x4.models import (
    Dataset,
    Habitat,
    HabitatModule,
    SaveGame,
    Sector,
    Station,
)


@pytest.mark.django_db
class TestSector:
    def test_create_sector(self, create_basic_sector):
        assert len(Sector.objects.all()) == 1

    @pytest.mark.usefixtures("_create_multiple_sectors")
    def test_cant_create_duplicates(self, create_save_game):
        with pytest.raises(IntegrityError):
            Sector.objects.create(
                name="sector0",
                game=create_save_game,
            )

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

    @pytest.mark.usefixtures("_create_multiple_stations")
    def test_cant_create_duplicates(
        self, create_save_game, create_basic_sector
    ):
        with pytest.raises(IntegrityError):
            Station.objects.create(
                name="station0",
                game=create_save_game,
                sector=create_basic_sector,
            )

    def test_station_str(self, create_station):
        assert str(create_station) == "Station Hammersmith"


@pytest.mark.django_db
class TestDataset:
    def test_create_dataset(self, create_dataset):
        assert len(Dataset.objects.all()) == 1

    def test_unique_constraint(self, create_dataset):
        with pytest.raises(IntegrityError):
            Dataset.objects.create(name="StarTrekin")

    def test_dataset_str(self, create_dataset):
        assert str(create_dataset) == "Dataset StarTrekin"


@pytest.mark.django_db
class TestHabitatModule:
    def test_create_habitat_module(self, create_habitat_module):
        assert len(HabitatModule.objects.all()) == 1

    def test_str(self, create_habitat_module):
        assert str(create_habitat_module) == "Habitat Borg Large"


@pytest.mark.django_db
class TestHabitats:
    def test_create_habitat(self, create_habitat):
        assert len(Habitat.objects.all()) == 1

    def test_str(self, create_habitat):
        assert str(create_habitat) == "Habitats Hammersmith Station Borg Large"
