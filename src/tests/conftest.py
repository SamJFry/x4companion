import pytest
from django.contrib.auth.models import User

from x4companion.x4.models import SaveGame, Sector


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
def create_save_game():
    user = User(username="CaptainKirk")
    user.save()
    game = SaveGame.objects.create(name="Kirk's x4 game", user=user)
    game.save()
    return game
