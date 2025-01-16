"""Contains the API views for the Data sets portion of the app.

These views allow management of data within a Dataset. Datasets contain the
data that all 'game' views reference.

"""

from django.db.models import QuerySet

from x4companion.x4.api_bases import X4APIBulkView, X4APISingleView
from x4companion.x4.models import (
    Dataset,
    FactoryModule,
    HabitatModule,
    SectorTemplate,
    Ware,
    WareOrder,
)
from x4companion.x4.serializers import (
    DatasetSerializer,
    FactoryModuleSerializer,
    HabitatModuleSerializer,
    SectorTemplateSerializer,
    WareOrdersSerializer,
    WareSerializer,
)


class Datasets(X4APIBulkView):
    """Manage all Datasets in the app."""

    serializer_class = DatasetSerializer

    def get_queryset(self) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return Dataset.objects.all()


class DatasetView(X4APISingleView):
    """Manage an individual dataset."""

    serializer_class = DatasetSerializer
    model_class = Dataset


class FactoryModules(X4APIBulkView):
    """Manage all Factory Modules."""

    serializer_class = FactoryModuleSerializer
    model_class = FactoryModule


class FactoryModuleView(X4APISingleView):
    """Manage an individual Factory Module."""

    serializer_class = FactoryModuleSerializer
    model_class = FactoryModule


class HabitatModules(X4APIBulkView):
    """Manage all Habitat Modules."""

    serializer_class = HabitatModuleSerializer
    model_class = HabitatModule


class HabitatModuleView(X4APISingleView):
    """Manage an individual Habitat Module."""

    serializer_class = HabitatModuleSerializer
    model_class = HabitatModule


class SectorTemplates(X4APIBulkView):
    """Manage sector templates for a dataset."""

    serializer_class = SectorTemplateSerializer
    model_class = SectorTemplate


class SectorTemplatesView(X4APISingleView):
    """Manage an individual sector template."""

    serializer_class = SectorTemplateSerializer
    model_class = SectorTemplate


class WareOrders(X4APIBulkView):
    """Manage sector templates for a dataset."""

    serializer_class = WareOrdersSerializer
    model_class = WareOrder


class WareOrderView(X4APISingleView):
    """Manage an individual ware order."""

    serializer_class = WareOrdersSerializer
    model_class = WareOrder


class Wares(X4APIBulkView):
    """Manage wares for a dataset."""

    serializer_class = WareSerializer
    model_class = Ware


class WareView(X4APISingleView):
    """Manage an individual ware."""

    serializer_class = WareSerializer
    model_class = Ware
