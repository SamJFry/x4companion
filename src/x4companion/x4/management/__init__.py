import dataclasses
import json
import pathlib


@dataclasses.dataclass
class Dataset:
    name: str
    sectors: list


def load_datasets(dataset_dir: pathlib.Path) -> list[Dataset]:
    datasets = dataset_dir.glob("*.json")
    loaded_sets = []
    for dset in datasets:
        with pathlib.Path.open(dset) as file:
            data = json.load(file)
        dataset = Dataset(
            name=dset.parts[-1].replace(".json", ""),
            sectors=data.get("sectors"),
        )
        loaded_sets.append(dataset)
    return loaded_sets
