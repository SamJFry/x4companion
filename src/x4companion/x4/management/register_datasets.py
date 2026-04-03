"""Methods and classes used to register datasets."""

import dataclasses
import json
import logging
import pathlib

from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
)
from rest_framework.serializers import BaseSerializer

from x4companion.x4.management.exceptions import (
    ObjectExistsError,
    ValidationError,
)
from x4companion.x4.management.logging import log_ok, log_warning
from x4companion.x4.models import Dataset
from x4companion.x4.serializers import (
    DatasetSerializer,
    FactoryModuleSerializer,
    HabitatModuleSerializer,
    SectorTemplateSerializer,
    WareOrdersSerializer,
    WareSerializer,
)

logger = logging.getLogger(__name__)


class SerializerToTableMappings:
    """Maps keys in dataset files to the serializers for their data."""

    factory_modules = FactoryModuleSerializer
    sectors = SectorTemplateSerializer
    wares = WareSerializer
    ware_orders = WareOrdersSerializer
    habitat_modules = HabitatModuleSerializer


class DatasetPrimaryKeys:
    """The primary key for each item type in dataset files."""

    factory_modules = "name"
    sectors = "name"
    wares = "name"
    habitat_modules = "name"


@dataclasses.dataclass
class DatasetTransaction:
    """Holds details of a dataset that is not yet in the DB.

    Attributes:
        name: The name of the Dataset.
        table_data: The data from the dataset we are writing.
        id_: Defaults to 0, but is replaced by the ID of the dataset once it
            has been created.

    """

    name: str
    table_data: dict[str, list[dict]]
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
            for key in self.transaction.table_data:
                RegisterTable(
                    serializer=getattr(SerializerToTableMappings, key),
                    table=key,
                    transaction=self.transaction,
                ).register_table()
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
        for key in self.transaction.table_data:
            RegisterTable(
                serializer=getattr(SerializerToTableMappings, key),
                table=key,
                transaction=self.transaction,
            ).update_table()


class RegisterTable:
    """A class to register/update a dataset table.

    Attributes:
        serializer: The serializer for the table.
        model: The django model the registration relates to.
        transaction: The transaction that is being completed.
        data: The incoming table data.
        table: The table name in the dataset file we are processing.

    """

    def __init__(
        self,
        serializer: type[BaseSerializer],
        table: str,
        transaction: DatasetTransaction,
    ) -> None:
        self.serializer = serializer
        self.model = serializer.Meta.model
        self.transaction = transaction
        self.data = transaction.table_data[table]
        self.table = table

    def _resolve_foreign_keys(self) -> list[dict]:
        """Resolve text relations in dataset dicts to usable foreign keys."""
        foreign_keys = [
            attribute
            for attribute in dir(self.model)
            if isinstance(
                getattr(self.model, attribute), ForwardManyToOneDescriptor
            )
            and attribute != "dataset"
        ]
        if not foreign_keys:
            return self.data
        for item in self.data:
            for key in foreign_keys:
                logger.debug("resolving foreign key '%s' for %s", key, item)
                related_model = getattr(self.model, key).field.related_model
                item[f"{key}_id"] = related_model.objects.get(
                    name=item[key]
                ).id
                item.pop(key)
        return self.data

    def register_table(self) -> None:
        """Register a new table of data in a dataset."""
        data = self._resolve_foreign_keys()
        serialized_data = self.serializer(
            data=data, many=True, context={"dataset_id": self.transaction.id_}
        )
        if not serialized_data.is_valid():
            raise ValidationError(serialized_data.errors)
        serialized_data.save()
        logger.info(
            "Registered %d items in table %s", len(self.data), self.table
        )

    def _update_item(self, item: dict) -> None:
        """Update individual DB items."""
        pk = getattr(DatasetPrimaryKeys, self.table)
        updated = self.serializer(
            self.model.objects.filter(
                **{pk: item[pk]}, dataset_id=self.transaction.id_
            ).first(),
            data=item,
            context={"dataset_id": self.transaction.id_},
        )
        if not updated.is_valid():
            raise ValidationError(updated.errors)
        updated.save()

    def update_table(self) -> None:
        """Updates existing tables with new data."""
        failed_count = 0
        data = self._resolve_foreign_keys()
        for item in data:
            try:
                self._update_item(item)
            except ValidationError:
                logger.exception(
                    "%s Could not update/create entry in table '%s', fix the "
                    "error then re-run the command.",
                    log_warning(),
                    self.table,
                )
                failed_count += 1
        success_count = len(self.data) - failed_count
        logger.info(
            "Registered %d items in %s table", success_count, self.table
        )
        if failed_count > 0:
            logger.info(
                "Failed to register %d items in %s table",
                failed_count,
                self.table,
            )


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
            table_data=data,
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
