"""Contains API views relating to Habitat Modules."""

from django.db.models import QuerySet

from x4companion.x4.models import HabitatModule
from x4companion.x4.serializers import HabitatModuleSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class HabitatModules(X4APIBulkView):
    """Manage all Habitat Modules."""

    serializer_class = HabitatModuleSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return HabitatModule.objects.filter(dataset=kwargs["dataset_id"])


class HabitatModuleView(X4APISingleView):
    """Manage an individual Habitat Module."""

    serializer_class = HabitatModuleSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return HabitatModule.objects.filter(
            id=kwargs["id_"], dataset=kwargs["dataset_id"]
        )
