"""Contains API views relating to sectors."""

from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from x4companion.x4.models import Sector
from x4companion.x4.serializers import SectorSerializer


class Sectors(APIView):
    """Manage sectors."""

    def get(self, request: HttpRequest) -> Response:
        """Get all sectors currently configured.

        Args:
            request: Get request made to this endpoint.

        Returns:
            A JSON response containing a list of sectors and their attributes.
        """
        serializer = SectorSerializer(Sector.objects.all(), many=True)
        return Response(
            {"sectors": serializer.data},
            status=status.HTTP_200_OK,
        )
