"""Contains API views relating to Factory Modules."""

from django.db.models import QuerySet

from x4companion.x4.models import FactoryModule
from x4companion.x4.serializers import FactoryModuleSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class FactoryModules(X4APIBulkView):
    """Manage all Factory Modules."""

    serializer_class = FactoryModuleSerializer
    model_class = FactoryModule


class FactoryModuleView(X4APISingleView):
    """Manage an individual Factory Module."""

    serializer_class = FactoryModuleSerializer
    model_class = FactoryModule
