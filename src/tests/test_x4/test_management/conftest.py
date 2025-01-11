import json
import pathlib

import pytest

from x4companion.x4.management import DatasetTransaction, register_datasets


@pytest.fixture
def create_test_dir():
    test_dir = pathlib.Path(__file__).parent / "test_dir"
    test_dir.mkdir()
    yield test_dir
    test_dir.rmdir()


@pytest.fixture
def create_test_sectors():
    return {
        "sectors": [
            {"name": f"sector_{x}", "sunlight_percent": 100} for x in range(10)
        ]
    }


@pytest.fixture
def create_good_data(create_test_dir, create_test_sectors):
    with pathlib.Path.open(
        create_test_dir / "test_dataset_0.json", "w"
    ) as file:
        json.dump(create_test_sectors, file)
    yield create_test_dir
    pathlib.Path.unlink(create_test_dir / "test_dataset_0.json")


@pytest.fixture
def register_data(create_good_data):
    register_datasets(create_good_data)
    return create_good_data


@pytest.fixture
def update_old_data(register_data):
    with pathlib.Path.open(register_data / "test_dataset_0.json", "r") as file:
        data = json.load(file)
    data["sectors"][9].update({"name": "sector_9", "sunlight_percent": 99})
    data["sectors"] += [
        {"name": "new_sector", "sunlight_percent": 1},
        {"name": "new_sector_2", "sunlight_percent": 2},
    ]
    pathlib.Path.unlink(register_data / "test_dataset_0.json")
    with pathlib.Path.open(register_data / "test_dataset_0.json", "w") as file:
        json.dump(data, file)
    return register_data


@pytest.fixture
def create_transaction():
    transaction = DatasetTransaction(
        name="test",
        sectors=[{"name": "good_sector", "sunlight_percent": 100}],
    )
    transaction.create_root()
    return transaction
