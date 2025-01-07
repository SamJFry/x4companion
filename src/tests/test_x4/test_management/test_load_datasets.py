import pytest

from x4companion.x4.management import load_datasets, DatasetTransaction
from x4companion.x4.management import ValidationError
from x4companion.x4.models import Dataset


def test_load_datasets(create_good_data):
    test_dataset = load_datasets(create_good_data)
    for index, dataset in enumerate(test_dataset):
        assert dataset.name == f"test_dataset_{index}"
        assert len(dataset.sectors) == 10

@pytest.mark.django_db
class TestDataset:
    def test_create_root(self):
        DatasetTransaction(name="test", sectors=[]).create_root()
        assert list(Dataset.objects.all().values()) == [{"id": 1, "name": "test"}]

    def test_create_root_raises_on_bad_name(self):
        with pytest.raises(ValidationError):
            DatasetTransaction(name="", sectors=[]).create_root()

