"""Contains views for Ware Orders."""

from django.db.models import QuerySet

from x4companion.x4.models import WareOrder
from x4companion.x4.serializers import WareOrdersSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class WareOrders(X4APIBulkView):
    """Manage sector templates for a dataset."""

    serializer_class = WareOrdersSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return WareOrder.objects.filter(ware__dataset=kwargs["dataset_id"])


class WareOrderView(X4APISingleView):
    """Manage an individual ware order."""

    serializer_class = WareOrdersSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return WareOrder.objects.filter(
            id=kwargs["id_"], ware__dataset=kwargs["dataset_id"]
        )
