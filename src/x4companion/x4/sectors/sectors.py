"""Contains API views relating to sectors."""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from x4companion.x4.models import Sector
from x4companion.x4.serializers import SectorSerializer


class Sectors(GenericAPIView):
    """Manage sectors."""
    serializer_class = SectorSerializer

    def get(self, request: Request) -> Response:
        """Get all sectors currently configured.

        Args:
            request: GET request made to this endpoint.

        Returns:
            A JSON response containing a list of sectors and their attributes.

        """
        serializer = self.serializer_class(Sector.objects.all(), many=True)
        return Response(
            {"sectors": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        """Creates a new sector in the database.

        Args:
            request: POST request with the json to create a new sector.

        Returns:
            JSON Response detailing the objectst that have been created.

        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
