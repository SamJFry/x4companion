"""Contains views for Ware Orders."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import WareOrder
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import WareOrdersSerializer


class WareOrders(GenericAPIView):
    """Manage sector templates for a dataset."""

    serializer_class = WareOrdersSerializer

    def post(self, request: Request, dataset_id: int) -> Response:
        """Create new Ware Orders.

        Args:
            request: POST request with the json to create new orders.
            dataset_id: The dataset you want to add the orders to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            self.serializer_class,
            request.data.get("data"),
            context={"dataset_id": dataset_id},
        )

    def get(self, request: Request, dataset_id: int) -> Response:
        """Get all available Ware Orders in the Dataset.

        Args:
            request: GET request made to this endpoint.
            dataset_id: The dataset you want to retrieve orders from.

        Returns:
            A JSON response containing a list of Ware Orders and their
            attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            WareOrder.objects.filter(ware__dataset=dataset_id),
        )