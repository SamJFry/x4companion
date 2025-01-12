import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from x4companion.x4.models import (
    Dataset,
    Factory,
    FactoryModule,
    Habitat,
    HabitatModule,
    SaveGame,
    Sector,
    SectorTemplate,
    Station,
    Ware,
    WareOrder,
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
def create_sector_template(create_dataset):
    template = SectorTemplate.objects.create(
        name="sector 001", dataset=create_dataset, sunlight_percent=100
    )
    template.save()
    return template


@pytest.fixture
def create_basic_sector(create_save_game, create_sector_template):
    sector = Sector.objects.create(
        template=create_sector_template, game=create_save_game
    )
    sector.save()
    return sector


@pytest.fixture
def _create_multiple_sector_templates(create_dataset):
    SectorTemplate.objects.bulk_create(
        [
            SectorTemplate(
                name=f"sector{x}", dataset=create_dataset, sunlight_percent=100
            )
            for x in range(4)
        ]
    )


@pytest.fixture
def _create_multiple_sectors(create_save_game, create_dataset):
    SectorTemplate.objects.bulk_create(
        [
            SectorTemplate(
                name=f"sector{x}", dataset=create_dataset, sunlight_percent=100
            )
            for x in range(4)
        ]
    )
    Sector.objects.bulk_create(
        [Sector(template_id=x, game=create_save_game) for x in range(1, 5)]
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
def create_user_2_sector_template(create_dataset):
    template = SectorTemplate.objects.create(
        name="Paris", dataset=create_dataset, sunlight_percent=100
    )
    template.save()
    return template


@pytest.fixture
def create_user_2_sector(
    create_user_2_save_game, create_user_2_sector_template
):
    sector = Sector.objects.create(
        template=create_user_2_sector_template, game=create_user_2_save_game
    )
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
def create_user_2_factory(create_user_2_station, create_factory_module):
    factory = Factory.objects.create(
        count=1, module=create_factory_module, station=create_user_2_station
    )
    factory.save()
    return factory


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


@pytest.fixture
def create_ware(create_dataset):
    ware = Ware(
        name="Stone",
        storage="S",
        dataset=create_dataset,
    )
    ware.save()
    return ware


@pytest.fixture
def create_factory_module(create_dataset, create_ware):
    module = FactoryModule.objects.create(
        name="Stone Factory",
        ware=create_ware,
        hourly_production=1000,
        hourly_energy=3600,
        dataset=create_dataset,
        workforce=1000,
    )
    module.save()
    return module


@pytest.fixture
def create_factory(create_factory_module, create_station):
    factory = Factory(
        count=5,
        module=create_factory_module,
        station=create_station,
    )
    factory.save()
    return factory


@pytest.fixture
def create_ware_order(create_ware, create_factory_module):
    ware_order = WareOrder(
        ware=create_ware, quantity=400, factory=create_factory_module
    )
    ware_order.save()
    return ware_order
