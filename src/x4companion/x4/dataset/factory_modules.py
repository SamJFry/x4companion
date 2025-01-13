"""Contains API views relating to Factory Modules."""

from django.db.models import QuerySet

from x4companion.x4.models import FactoryModule
from x4companion.x4.serializers import FactoryModuleSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class FactoryModules(X4APIBulkView):
    """Manage all Factory Modules."""

    serializer_class = FactoryModuleSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return FactoryModule.objects.filter(dataset=kwargs["dataset_id"])


class FactoryModuleView(X4APISingleView):
    """Manage an individual Factory Module."""

    serializer_class = FactoryModuleSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return FactoryModule.objects.filter(
            id=kwargs["id_"], dataset=kwargs["dataset_id"]
        )
