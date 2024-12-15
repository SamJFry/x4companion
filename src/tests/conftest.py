import pytest
from django.contrib.auth.models import User

from x4companion.x4.models import SaveGame, Sector, Station


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
def authed_client(client, create_user):
    client.force_login(create_user)
    return client


@pytest.fixture
def authed_client_2(client, create_user_2):
    client.force_login(create_user_2)
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
def _create_multiple_saves(create_user):
    SaveGame.objects.bulk_create(
        [SaveGame(name=f"game_{x}", user=create_user) for x in range(3)]
    )


@pytest.fixture
def create_save_game(create_user):
    game = SaveGame.objects.create(name="Kirk's x4 game", user=create_user)
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
def create_user_2_save_game(create_user_2):
    game = SaveGame.objects.create(name="Spock's x4 game", user=create_user_2)
    game.save()
    return game
