"""Contains views for Ware Orders."""

from x4companion.x4.models import WareOrder
from x4companion.x4.serializers import WareOrdersSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class WareOrders(X4APIBulkView):
    """Manage sector templates for a dataset."""

    serializer_class = WareOrdersSerializer
    model_class = WareOrder


class WareOrderView(X4APISingleView):
    """Manage an individual ware order."""

    serializer_class = WareOrdersSerializer
    model_class = WareOrder
