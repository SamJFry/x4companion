"""Contains views for Sector Templates."""

from django.db.models import QuerySet

from x4companion.x4.models import SectorTemplate
from x4companion.x4.serializers import SectorTemplateSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class SectorTemplates(X4APIBulkView):
    """Manage sector templates for a dataset."""

    serializer_class = SectorTemplateSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return SectorTemplate.objects.filter(dataset=kwargs["dataset_id"])


class SectorTemplatesView(X4APISingleView):
    """Manage an individual sector template."""

    serializer_class = SectorTemplateSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return SectorTemplate.objects.filter(
            id=kwargs["id_"], dataset=kwargs["dataset_id"]
        )
