"""Methods and classes used to register datasets."""

import dataclasses
import json
import logging
import pathlib

from x4companion.x4.management.exceptions import (
    ObjectExistsError,
    ValidationError,
)
from x4companion.x4.management.logging import log_ok
from x4companion.x4.models import Dataset
from x4companion.x4.serializers import (
    DatasetSerializer,
    SectorTemplateSerializer,
)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DatasetTransaction:
    """Holds details of a dataset that is not yet in the DB.

    Attributes:
        name: The name of the Dataset.
        sectors: The sectors in the dataset.
        id_: Defaults to 0, but is replaced by the ID of the dataset once it
            has been created.

    """

    name: str
    sectors: list[dict]
    id_: int = 0

    def create_root(self) -> None:
        """Create the Dataset in the Dataset model."""
        dataset = DatasetSerializer(data={"name": self.name}, many=False)
        if not dataset.is_valid():
            raise ValidationError(dataset.errors)
        self.id_ = dataset.save().id

    def rollback(self) -> None:
        """Deletes the dataset."""
        Dataset.objects.get(name=self.name).delete()


class RegisterDataset:
    """Used to register a dataset in the application.

    Attributes:
        transaction: The Dataset we are registering.

    """

    def __init__(self, transaction: DatasetTransaction) -> None:
        self.transaction = transaction

    def register(self) -> None:
        """Register the Dataset."""
        try:
            logger.info("Registering dataset: %s", self.transaction.name)
            self.transaction.create_root()
            self.create_sectors()
            logger.info(
                "%s Registered dataset %s", log_ok(), self.transaction.name
            )
        except ValidationError:
            logger.exception(
                "Error registering dataset: %s", self.transaction.name
            )
            self.transaction.rollback()
        except ObjectExistsError:
            logger.info("%s already registered", self.transaction.name)

    def create_sectors(self) -> None:
        """Create the sectors in the SectorsTemplate model."""
        sectors = SectorTemplateSerializer(
            data=self.transaction.sectors,
            many=True,
            context={"dataset_id": self.transaction.id_},
        )
        if not sectors.is_valid():
            raise ValidationError(sectors.errors)
        sectors.save()
        logger.info("Registered %d sectors", len(self.transaction.sectors))


def collect_datasets(dataset_dir: pathlib.Path) -> list[DatasetTransaction]:
    """Collects all available datasets from the given directory.

    Any `.json` file in the directory is considered a dataset and is collected
    and loaded.

    Args:
        dataset_dir: The directory to collect datasets from.

    Returns:
        A list of datasets loaded into a processable transaction.
    """
    logger.info("Collecting datasets from %s", str(dataset_dir))
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
    logger.info("Collected %d datasets", len(loaded_sets))
    return loaded_sets


def register_datasets(dataset_dir: pathlib.Path) -> None:
    """Collects new datasets and registers them in the application.

    Args:
        dataset_dir: The directory to collect datasets from.

    """
    sets = collect_datasets(dataset_dir)
    for dataset in sets:
        RegisterDataset(dataset).register()
