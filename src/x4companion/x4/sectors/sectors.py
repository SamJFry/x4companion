"""Contains API views relating to sectors."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from x4companion.x4.models import Sector
from x4companion.x4.serializers import SectorSerializer, SectorsSerializer


class Sectors(GenericAPIView):
    """Manage multiple sectors."""

    serializer_class = SectorsSerializer

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
            JSON Response detailing the objects that have been created.

        """
        serializer = self.serializer_class(data=request.data.get("data"))
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.create(serializer.data)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class SectorView(APIView):
    """Manage an individual Sector."""

    serializer_class = SectorsSerializer

    def get(self, request: Request, id_: int) -> Response:
        """Get a single sector.

        Args:
            request: GET request.
            id_: The ID of the sector to get.

        Returns:
            A JSON response for a single sector.

        """
        serializer = self.serializer_class(Sector.objects.get(id=id_))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, name: str) -> Response:
        """Create a sector

        Args:
            request: POST request.
            name: The name of the sector to create

        Returns:
            A JSON response of the created object.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, id_: int) -> Response:
        """Delete a sector from the Database.

        Args:
            request: DELETE Request.
            id_: The id of the sector to delete.

        Returns:
            An empty response if the sector has been deleted.

        """
        Sector.objects.filter(id=id_).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
