"""Contains the command to register Datasets."""

import pathlib

from django.core.management.base import BaseCommand
from django.conf import settings

from x4companion.x4.management import register_datasets


class Command(BaseCommand):
    """Register all available Datasets in the datasets directory.

    By default, it checks in `/x4companion/datasets` but the directory can be
    overridden by setting settings.DATASETS_PATH.

    """
    help = "Registers all dataset files in the datasets directory"

    def handle(self, *args, **kwargs) -> None:
        register_datasets(settings.DATASETS_PATH)
