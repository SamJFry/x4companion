"""Methods and classes used to register datasets."""

import dataclasses
import json
import logging
import pathlib

from rest_framework.serializers import BaseSerializer

from x4companion.x4.management.exceptions import (
    ObjectExistsError,
    ValidationError,
)
from x4companion.x4.management.logging import log_ok, log_warning
from x4companion.x4.models import Dataset, SectorTemplate
from x4companion.x4.serializers import (
    DatasetSerializer,
    SectorTemplateSerializer,
    WareSerializer,
)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DatasetTransaction:
    """Holds details of a dataset that is not yet in the DB.

    Attributes:
        name: The name of the Dataset.
        sectors: The sectors in the dataset.
        wares: The wares in the dataset.
        id_: Defaults to 0, but is replaced by the ID of the dataset once it
            has been created.

    """

    name: str
    sectors: list[dict]
    wares: list[dict]
    id_: int = 0

    def create_root(self) -> None:
        """Create the Dataset in the Dataset model."""
        dataset = DatasetSerializer(data={"name": self.name}, many=False)
        if not dataset.is_valid():
            raise ValidationError(dataset.errors)
        self.id_ = dataset.save().id

    def get_existing_id(self) -> None:
        """Set the ID to be that of the existing dataset.

        This should only be used when updating an existing dataset.

        Raises:
            Dataset.DoesNotExist: The dataset you referenced does not exist in
                the DB.

        """
        self.id_ = Dataset.objects.get(name=self.name).id

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
            self.create_wares()
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

    def update(self) -> None:
        """Updates a dataset that exists in the DB already."""
        self.transaction.get_existing_id()
        self.update_sectors()

    def _register_key(
        self, serializer: type[BaseSerializer], data: list[dict]
    ) -> None:
        """Register a key from the dataset."""
        serialized_data = serializer(
            data=data, many=True, context={"dataset_id": self.transaction.id_}
        )
        if not serialized_data.is_valid():
            raise ValidationError(serialized_data.errors)
        serialized_data.save()

    def create_sectors(self) -> None:
        """Create the sectors in the SectorsTemplate model."""
        self._register_key(SectorTemplateSerializer, self.transaction.sectors)
        logger.info("Registered %d sectors", len(self.transaction.sectors))

    def create_wares(self) -> None:
        """Create the wares in the Ware model."""
        self._register_key(WareSerializer, self.transaction.wares)
        logger.info("Registered %d wares", len(self.transaction.wares))

    def update_sectors(self) -> None:
        """Updates fields on existing sectors.

        If a sector does not exist, it is created.

        """
        failed_sectors = 0
        for sector in self.transaction.sectors:
            try:
                self._update_sector(sector)
            except ValidationError:
                logger.exception(
                    "%s Could not update/create sector, fix the error then "
                    "re-run the command.",
                    log_warning(),
                )
                failed_sectors += 1
        logger.info("Registered %d sectors", len(self.transaction.sectors))
        if failed_sectors > 0:
            logger.info("Failed to register %d sectors", failed_sectors)

    def _update_sector(self, sector: dict) -> None:
        """Run updates on an individual sector."""
        updated = SectorTemplateSerializer(
            SectorTemplate.objects.filter(
                name=sector["name"], dataset_id=self.transaction.id_
            ).first(),
            data=sector,
            context={"dataset_id": self.transaction.id_},
        )
        if not updated.is_valid():
            raise ValidationError(updated.errors)
        updated.save()


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
            wares=data.get("wares"),
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


def update_datasets(dataset_dir: pathlib.Path) -> None:
    """Collects datasets and updates the ones that exist in the DB.

    New Datasets are not registered.

    Args:
        dataset_dir: The directory to collect datasets from.

    """
    sets = collect_datasets(dataset_dir)
    for dataset in sets:
        RegisterDataset(dataset).update()
