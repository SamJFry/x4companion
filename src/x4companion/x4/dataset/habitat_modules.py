"""Contains API views relating to Habitat Modules."""

from django.db.models import QuerySet

from x4companion.x4.models import HabitatModule
from x4companion.x4.serializers import HabitatModuleSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class HabitatModules(X4APIBulkView):
    """Manage all Habitat Modules."""

    serializer_class = HabitatModuleSerializer
    model_class = HabitatModule


class HabitatModuleView(X4APISingleView):
    """Manage an individual Habitat Module."""

    serializer_class = HabitatModuleSerializer
    model_class = HabitatModule