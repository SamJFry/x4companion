import json
import pathlib

import pytest


@pytest.fixture
def create_test_dir():
    test_dir = pathlib.Path(__file__).parent / "test_dir"
    test_dir.mkdir()
    yield test_dir
    test_dir.rmdir()


@pytest.fixture
def create_good_data(create_test_dir):
    with pathlib.Path.open(
        create_test_dir / "test_dataset_0.json", "w"
    ) as file:
        json.dump(
            {
                "sectors": [
                    {"name": f"sector_{x}", "sunlight_percent": 100}
                    for x in range(10)
                ]
            },
            file,
        )
    yield create_test_dir
    pathlib.Path.unlink(create_test_dir / "test_dataset_0.json")
