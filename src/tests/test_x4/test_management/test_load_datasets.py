import pytest

from x4companion.x4.management import (
    DatasetTransaction,
    RegisterDataset,
    ValidationError,
    collect_datasets,
)
from x4companion.x4.models import Dataset, SectorTemplate


def test_collect_datasets(create_good_data):
    test_dataset = collect_datasets(create_good_data)
    for index, dataset in enumerate(test_dataset):
        assert dataset.name == f"test_dataset_{index}"
        assert len(dataset.sectors) == 10


@pytest.mark.django_db
class TestDataset:
    def test_create_root(self, create_transaction):
        assert list(Dataset.objects.all().values()) == [
            {"id": 1, "name": "test"}
        ]
        assert create_transaction.id_ == 1

    def test_create_root_raises_on_bad_name(self):
        with pytest.raises(ValidationError):
            DatasetTransaction(name="", sectors=[]).create_root()

    def test_rollback(self, create_dataset):
        transaction = DatasetTransaction(name="StarTrekin", sectors=[])
        transaction.rollback()
        assert list(Dataset.objects.all().values()) == []


@pytest.mark.django_db
class TestRegisterDataset:
    def test_create_sectors(self, create_transaction):
        RegisterDataset(create_transaction).create_sectors()
        assert list(SectorTemplate.objects.all().values()) == [
            {
                "id": 1,
                "name": "good_sector",
                "sunlight_percent": 100,
                "dataset_id": 1,
            }
        ]

    def test_create_sectors_raises_on_bad_data(self, create_transaction):
        create_transaction.sectors = [{"name": "just a name"}]
        with pytest.raises(ValidationError):
            RegisterDataset(create_transaction).create_sectors()

    def test_register(self, create_good_data):
        dataset = DatasetTransaction(
            name="test", sectors=[{"name": "s1", "sunlight_percent": 1}]
        )
        RegisterDataset(dataset).register()
        assert list(Dataset.objects.all().values()) == [
            {"id": 1, "name": "test"}
        ]
        assert list(SectorTemplate.objects.all().values()) == [
            {
                "id": 1,
                "name": "s1",
                "sunlight_percent": 1,
                "dataset_id": 1,
            }
        ]

    def test_register_handles_already_registered(
        self, create_good_data, create_dataset
    ):
        dataset = DatasetTransaction(name="StarTrekin", sectors=[])
        RegisterDataset(dataset).register()
        assert Dataset.objects.count() == 1

    def test_register_rollback_on_sector_error(self):
        dataset = DatasetTransaction(name="test", sectors=[{"name": "s1"}])
        RegisterDataset(dataset).register()
        assert Dataset.objects.count() == 0
