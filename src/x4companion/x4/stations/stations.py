"""Contains API views relating to Stations."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame, Station
from x4companion.x4.responses import delete_response, get_response
from x4companion.x4.serializers import (
    StationSerializerRead,
    StationSerializerWrite,
)


class Stations(GenericAPIView):
    """Manage multiple stations."""

    def post(self, request: Request, save_id: int) -> Response:
        """Create new stations.

        Args:
            request: POST request with the json to create new stations.
            save_id: The ID of the save game the stations belong to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        serializer = StationSerializerWrite(
            data=request.data.get("data"),
            many=True,
            context={"save_id": save_id},
        )
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def get(self, request: Request, save_id: int) -> Response:
        """Get all stations currently configured.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game the stations belong to.

        Returns:
            A JSON response containing a list of stations and their attributes.

        """
        game = SaveGame.objects.get(id=save_id)
        serializer = StationSerializerRead(game.station_set.all(), many=True)
        return Response(
            {"stations": serializer.data},
            status=status.HTTP_200_OK,
        )


class StationView(GenericAPIView):
    """Manage a specific station."""

    def delete(self, request: Request, save_id: int, id_: int) -> Response:
        """Delete a staion.

        Args:
            request: DELETE Request.
            save_id: The ID of the save game the station belong to.
            id_: The id of the station to delete.

        Returns:
            An empty response if the station been deleted.

        """
        return delete_response(Station, id_, game=save_id)

    def get(self, request: Request, save_id: int, id_: int) -> Response:
        """Get a single sector.

        Args:
            request: GET request.
            save_id: The ID of the save game the station belongs to.
            id_: The ID of the station to get.

        Returns:
            A JSON response for a single station.

        """
        return get_response(Station, StationSerializerRead, id_, game=save_id)
