import dataclasses
import json
import logging
import pathlib

from colorama import Fore

from x4companion.x4.management.exceptions import (
    ObjectExistsError,
    ValidationError,
)
from x4companion.x4.models import Dataset
from x4companion.x4.serializers import (
    DatasetSerializer,
    SectorTemplateSerializer,
)

logger = logging.getLogger(__name__)


def log_ok() -> str:
    return "[" + Fore.GREEN + " OK " + Fore.RESET + "]"


@dataclasses.dataclass
class DatasetTransaction:
    name: str
    sectors: list[dict]
    id_: int = 0

    def create_root(self) -> None:
        dataset = DatasetSerializer(data={"name": self.name}, many=False)
        if not dataset.is_valid():
            raise ValidationError(dataset.errors)
        self.id_ = dataset.save().id

    def rollback(self) -> None:
        Dataset.objects.get(name=self.name).delete()


class RegisterDataset:
    def __init__(self, transaction: DatasetTransaction) -> None:
        self.transaction = transaction

    def register(self) -> None:
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
    sets = collect_datasets(dataset_dir)
    for dataset in sets:
        RegisterDataset(dataset).register()
