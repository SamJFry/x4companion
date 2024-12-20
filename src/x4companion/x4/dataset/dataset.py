"""Contains API views relating to Data sets."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import Dataset
from x4companion.x4.responses import (
    get_bulk_response,
    post_response,
)
from x4companion.x4.serializers import DatasetSerializer


class Datasets(GenericAPIView):
    """Manage all Datasets in the app."""

    serializer_class = DatasetSerializer

    def post(self, request: Request) -> Response:
        """Create new Datasets in the app.

        Args:
            request: The incoming POST request.

        returns:
            A DRF response with the created objects.

        """
        return post_response(self.serializer_class, request.data.get("data"))

    def get(self, request: Request) -> Response:
        """Get all the currently configured Datasets.

        Args:
            request: The incoming GET request.

        returns:
            A DRF response with the existing objects.

        """
        return get_bulk_response(
            request, self.serializer_class, Dataset.objects.all()
        )
