"""Contains the command to register Datasets."""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from x4companion.x4.management import register_datasets, update_datasets


class Command(BaseCommand):
    """Register all available Datasets in the datasets directory.

    By default, it checks in `/x4companion/datasets` but the directory can be
    overridden by setting settings.DATASETS_PATH.

    """

    help = "Registers all dataset files in the datasets directory"

    def add_arguments(self, parser: CommandParser) -> None:
        """Additional command options."""
        parser.add_argument("--update", action="store_true")

    def handle(self, *args, **options) -> None:
        """Runs the command."""
        if options["update"]:
            update_datasets(settings.DATASETS_PATH)
            return
        register_datasets(settings.DATASETS_PATH)
