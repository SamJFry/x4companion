"""Contains API views relating to sectors."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from x4companion.x4.models import SaveGame, Sector
from x4companion.x4.serializers import SectorSerializer, SectorsSerializer


class Sectors(GenericAPIView):
    """Manage multiple sectors."""

    serializer_class = SectorsSerializer

    def get(self, request: Request, save_id: int) -> Response:
        """Get all sectors currently configured.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game the sectors belong to.

        Returns:
            A JSON response containing a list of sectors and their attributes.

        """
        game = SaveGame.objects.get(id=save_id)
        serializer = SectorSerializer(game.sector_set.all(), many=True)
        return Response(
            {"sectors": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request, save_id: int) -> Response:
        """Creates a new sector in the database.

        Args:
            request: POST request with the json to create a new sector.
            save_id: The ID of the save game the sectors belong to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        serializer = self.serializer_class(
            data=request.data.get("data"), context={"game": save_id}
        )
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.create(serializer.data)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class SectorView(APIView):
    """Manage an individual Sector."""

    serializer_class = SectorsSerializer

    def get(self, request: Request, save_id: int, id_: int) -> Response:
        """Get a single sector.

        Args:
            request: GET request.
            save_id: The ID of the save game the sector belongs to.
            id_: The ID of the sector to get.

        Returns:
            A JSON response for a single sector.

        """
        serializer = self.serializer_class(
            Sector.objects.filter(id=id_, game=save_id)
        )
        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data[0], status=status.HTTP_200_OK)

    def delete(self, request: Request, save_id: int, id_: int) -> Response:
        """Delete a sector from the Database.

        Args:
            request: DELETE Request.
            save_id: The ID of the save game the sector belong to.
            id_: The id of the sector to delete.

        Returns:
            An empty response if the sector has been deleted.

        """
        deleted = Sector.objects.filter(id=id_, game=save_id).delete()[0]
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
