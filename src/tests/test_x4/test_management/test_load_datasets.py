import pytest

from x4companion.x4.management import load_datasets, DatasetTransaction, RegisterDatasets
from x4companion.x4.management import ValidationError
from x4companion.x4.models import Dataset, SectorTemplate


def test_load_datasets(create_good_data):
    test_dataset = load_datasets(create_good_data)
    for index, dataset in enumerate(test_dataset):
        assert dataset.name == f"test_dataset_{index}"
        assert len(dataset.sectors) == 10


@pytest.mark.django_db
class TestDataset:
    def test_create_root(self):
        transaction = DatasetTransaction(name="test", sectors=[])
        transaction.create_root()
        assert list(Dataset.objects.all().values()) == [
            {"id": 1, "name": "test"}
        ]
        assert transaction.dataset_id == 1

    def test_create_root_raises_on_bad_name(self):
        with pytest.raises(ValidationError):
            DatasetTransaction(name="", sectors=[]).create_root()

    def test_rollback(self, create_dataset):
        transaction = DatasetTransaction(name="StarTrekin", sectors=[])
        transaction.rollback()
        assert list(Dataset.objects.all().values()) == []

@pytest.mark.django_db
class TestRegisterDataset:
    def test_create_sectors(self):
        transaction = DatasetTransaction(name="test", sectors=[
            {"name": "good_sector", "sunlight_percent": 100}
        ])
        transaction.create_root()
        RegisterDatasets(transaction).create_sectors()
        assert list(SectorTemplate.objects.all().values()) == [
            {"name": "good", "sunlight_percent": 100, "dataset_id": 1}
        ]
