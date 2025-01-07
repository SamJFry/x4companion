import dataclasses
import json
import pathlib

from x4companion.x4.serializers import DatasetSerializer
from x4companion.x4.management.exceptions import ValidationError
from x4companion.x4.models import Dataset


@dataclasses.dataclass
class DatasetTransaction:
    name: str
    sectors: list

    def create_root(self):
        dataset = DatasetSerializer(data={"name": self.name})
        if not dataset.is_valid():
            raise ValidationError(dataset.errors)
        dataset.save()

    def rollback(self):
        Dataset.objects.get(name=self.name).delete()


def load_datasets(dataset_dir: pathlib.Path) -> list[DatasetTransaction]:
    datasets = dataset_dir.glob("*.json")
    loaded_sets = []
    for dset in datasets:
        with pathlib.Path.open(dset) as file:
            data = json.load(file)
        dataset = DatasetTransaction(
            name=dset.parts[-1].replace(".json", ""),
            sectors=data.get("sectors"),
        )
        loaded_sets.append(dataset)
    return loaded_sets
