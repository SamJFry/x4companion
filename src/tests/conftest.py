import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from x4companion.x4.models import (
    Dataset,
    Habitat,
    HabitatModule,
    SaveGame,
    Sector,
    Station,
)


@pytest.fixture
def create_user():
    user = User(username="CaptainKirk")
    user.save()
    return user


@pytest.fixture
def create_user_2():
    user = User(username="CmdSpock")
    user.save()
    return user


@pytest.fixture
def authed_client(create_user):
    client = APIClient()
    client.force_authenticate(create_user)
    return client


@pytest.fixture
def authed_client_2(create_user_2):
    client = APIClient()
    client.force_authenticate(create_user_2)
    return client


@pytest.fixture
def create_basic_sector(create_save_game):
    sector = Sector.objects.create(name="sector 001", game=create_save_game)
    sector.save()
    return sector


@pytest.fixture
def _create_multiple_sectors(create_save_game):
    Sector.objects.bulk_create(
        [Sector(name=f"sector{x}", game=create_save_game) for x in range(4)]
    )


@pytest.fixture
def _create_multiple_saves(create_user, create_dataset):
    SaveGame.objects.bulk_create(
        [
            SaveGame(
                name=f"game_{x}", user=create_user, dataset=create_dataset
            )
            for x in range(3)
        ]
    )


@pytest.fixture
def create_save_game(create_user, create_dataset):
    game = SaveGame.objects.create(
        name="Kirk's x4 game", user=create_user, dataset=create_dataset
    )
    game.save()
    return game


@pytest.fixture
def create_station(create_basic_sector, create_save_game):
    station = Station.objects.create(
        name="Hammersmith", game=create_save_game, sector=create_basic_sector
    )
    station.save()
    return station


@pytest.fixture
def _create_multiple_stations(create_basic_sector, create_save_game):
    Station.objects.bulk_create(
        [
            Station(
                name=f"station{x}",
                game=create_save_game,
                sector=create_basic_sector,
            )
            for x in range(3)
        ]
    )


@pytest.fixture
def create_user_2_save_game(create_user_2, create_dataset):
    game = SaveGame.objects.create(
        name="Spock's x4 game", user=create_user_2, dataset=create_dataset
    )
    game.save()
    return game


@pytest.fixture
def create_user_2_sector(create_user_2_save_game):
    sector = Sector.objects.create(name="Paris", game=create_user_2_save_game)
    sector.save()
    return sector


@pytest.fixture
def create_user_2_station(create_user_2_save_game, create_user_2_sector):
    station = Station.objects.create(
        name="La Chapelle",
        game=create_user_2_save_game,
        sector=create_user_2_sector,
    )
    station.save()
    return station


@pytest.fixture
def create_user_2_habitat(create_user_2_station, create_habitat_module):
    habitat = Habitat.objects.create(
        count=1, module=create_habitat_module, station=create_user_2_station
    )
    habitat.save()
    return habitat


@pytest.fixture
def create_dataset():
    dataset = Dataset.objects.create(name="StarTrekin")
    dataset.save()
    return dataset


@pytest.fixture
def create_habitat_module(create_dataset):
    module = HabitatModule.objects.create(
        name="Borg Large",
        capacity=1000,
        species="borg",
        dataset=create_dataset,
    )
    module.save()
    return module


@pytest.fixture
def create_habitat(create_station, create_habitat_module):
    habitat = Habitat.objects.create(
        count=1, module=create_habitat_module, station=create_station
    )
    habitat.save()
    return habitat
