from x4companion.x4.management import load_datasets


def test_load_datasets(create_good_data):
    test_dataset = load_datasets(create_good_data)
    for index, dataset in enumerate(test_dataset):
        assert dataset.name == f"test_dataset_{index}"
        assert len(dataset.sectors) == 10
