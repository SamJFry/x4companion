import logging

import pytest

from x4companion.x4.management import (
    DatasetTransaction,
    RegisterDataset,
    collect_datasets,
    update_datasets,
)
from x4companion.x4.management.exceptions import ValidationError
from x4companion.x4.models import Dataset, FactoryModule, SectorTemplate, Ware

logger = logging.getLogger("x4companion.x4.management.register_datasets")


def test_collect_datasets(create_good_data):
    test_dataset = collect_datasets(create_good_data)
    for index, dataset in enumerate(test_dataset):
        assert dataset.name == f"test_dataset_{index}"
        assert len(dataset.sectors) == 10


@pytest.mark.django_db
def test_register_datasets(register_data):
    assert Dataset.objects.count() == 1


@pytest.mark.django_db
def test_update_datasets(update_old_data):
    update_datasets(update_old_data)
    updated_sector_sunlight = (
        Dataset.objects.get(id=1)
        .sectortemplate_set.get(name="sector_9")
        .sunlight_percent
    )
    assert updated_sector_sunlight == 99
    assert SectorTemplate.objects.get(name="new_sector")
    assert SectorTemplate.objects.get(name="new_sector_2")


@pytest.mark.django_db
class TestDataset:
    def test_create_root(self, create_transaction):
        assert list(Dataset.objects.all().values()) == [
            {"id": 1, "name": "test"}
        ]
        assert create_transaction.id_ == 1

    def test_create_root_raises_on_bad_name(self):
        with pytest.raises(ValidationError):
            DatasetTransaction(
                name="", sectors=[], wares=[], factories=[]
            ).create_root()

    def test_rollback(self, create_dataset):
        transaction = DatasetTransaction(
            name="StarTrekin", sectors=[], wares=[], factories=[]
        )
        transaction.rollback()
        assert list(Dataset.objects.all().values()) == []


@pytest.mark.django_db
class TestRegisterDataset:
    def test_create_sectors_raises_on_bad_data(self, create_transaction):
        create_transaction.sectors = [{"name": "just a name"}]
        with pytest.raises(ValidationError):
            RegisterDataset(create_transaction).create_sectors()

    def test_register(self, transaction_data):
        dataset = DatasetTransaction(table_data=transaction_data, name="test")
        RegisterDataset(dataset).register()
        assert list(Dataset.objects.all().values()) == [
            {"id": 1, "name": "test"}
        ]
        assert list(Ware.objects.all().values()) == [
            {
                "id": 1,
                "name": "Stem Bolts",
                "storage": "C",
                "volume": 1,
                "dataset_id": 1,
            }
        ]
        assert list(FactoryModule.objects.all().values()) == [
            {
                "id": 1,
                "name": "Stem Bolt Factory",
                "ware_id": 1,
                "hourly_production": 5000,
                "hourly_energy": 1000,
                "workforce": 225,
                "dataset_id": 1,
            }
        ]
        assert list(SectorTemplate.objects.all().values()) == [
            {
                "id": 1,
                "name": "good_sector",
                "sunlight_percent": 100,
                "dataset_id": 1,
            }
        ]

    def test_register_handles_already_registered(self, create_dataset):
        dataset = DatasetTransaction(name="StarTrekin", table_data={})
        RegisterDataset(dataset).register()
        assert Dataset.objects.count() == 1

    def test_register_rollback_on_sector_error(self):
        dataset = DatasetTransaction(
            name="test", table_data={"sectors": [{"name": "s1"}]}
        )
        RegisterDataset(dataset).register()
        assert Dataset.objects.count() == 0

    def test_update_sectors_handles_bad_sector(
        self, register_data, create_test_data, caplog
    ):
        sectors = create_test_data["sectors"]
        del sectors[8]["sunlight_percent"]
        dataset = DatasetTransaction(
            name="test_dataset_0", table_data={"sectors": sectors}
        )
        RegisterDataset(dataset).update()
        assert caplog.records[0].levelname == "ERROR"
