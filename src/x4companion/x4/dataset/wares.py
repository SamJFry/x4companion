"""Contains views for accessing Wares."""

from django.db.models import QuerySet

from x4companion.x4.models import Ware
from x4companion.x4.serializers import WareSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class Wares(X4APIBulkView):
    """Manage wares for a dataset."""

    serializer_class = WareSerializer
    model_class = Ware


class WareView(X4APISingleView):
    """Manage an individual ware."""

    serializer_class = WareSerializer
    model_class = Ware