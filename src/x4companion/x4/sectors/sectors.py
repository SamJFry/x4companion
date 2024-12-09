"""Contains API views relating to sectors."""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from x4companion.x4.models import Sector
from x4companion.x4.serializers import SectorSerializer


class Sectors(APIView):
    """Manage sectors."""

    def get(self, request: Request) -> Response:
        """Get all sectors currently configured.

        Args:
            request: GET request made to this endpoint.

        Returns:
            A JSON response containing a list of sectors and their attributes.

        """
        serializer = SectorSerializer(Sector.objects.all(), many=True)
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
        serializer = SectorSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
