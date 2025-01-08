import pathlib

from django.core.management.base import BaseCommand

from x4companion.x4.management import register_datasets


class Command(BaseCommand):
    help = "Registers all dataset files in the datasets directory"

    def handle(self, *args, **kwargs):
        register_datasets(pathlib.Path(__file__).parents[3] / "datasets")

