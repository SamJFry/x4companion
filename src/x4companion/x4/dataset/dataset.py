"""Contains API views relating to Data sets."""

from django.db.models import QuerySet

from x4companion.x4.models import Dataset
from x4companion.x4.serializers import DatasetSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class Datasets(X4APIBulkView):
    """Manage all Datasets in the app."""

    serializer_class = DatasetSerializer

    def get_queryset(self) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return Dataset.objects.all()


class DatasetView(X4APISingleView):
    """Manage an individual dataset."""

    serializer_class = DatasetSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return Dataset.objects.filter(id=kwargs["id_"])
