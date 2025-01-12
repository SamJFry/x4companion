"""Contains views for accessing Wares."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import Ware
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import WareSerializer


class Wares(GenericAPIView):
    """Manage wares for a dataset."""

    serializer_class = WareSerializer

    def post(self, request: Request, dataset_id: int) -> Response:
        """Create new Wares.

        Args:
            request: POST request with the json to create new wares.
            dataset_id: The dataset you want to add the template to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            self.serializer_class,
            request.data.get("data"),
            context={"dataset_id": dataset_id},
        )

    def get(self, request: Request, dataset_id: int) -> Response:
        """Get all available Wares in the Dataset.

        Args:
            request: GET request made to this endpoint.
            dataset_id: The dataset you want to retrieve wares from.

        Returns:
            A JSON response containing a list of wares and their attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            Ware.objects.filter(dataset=dataset_id),
        )


class WareView(GenericAPIView):
    """Manage an individual sector template."""

    serializer_class = WareSerializer

    def get(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Get a single Ware.

        Args:
            request: The incoming GET request.
            dataset_id: The ID of the dataset the ware belongs to.
            id_: The ID of the ware.

        Returns:
            A JSON Response containing the requested ware.

        """
        return get_response(
            self.serializer_class,
            Ware.objects.filter(id=id_, dataset=dataset_id),
        )

    def delete(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Delete a Ware.

        Args:
            request: The incoming DELETE request.
            dataset_id: The dataset the ware belongs to.
            id_: The ID of the template.

        Returns:
            An empty response if the ware has been deleted.

        """
        return delete_response(Ware.objects.filter(id=id_, dataset=dataset_id))
