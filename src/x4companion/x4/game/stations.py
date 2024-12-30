"""Contains API views relating to Stations."""

from http import HTTPMethod

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame, Station
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import (
    StationSerializerRead,
    StationSerializerWrite,
)


class Stations(GenericAPIView):
    """Manage multiple stations."""

    def get_serializer_class(
        self,
    ) -> type[StationSerializerRead] | type[StationSerializerWrite]:
        """Returns correct serializer for the request type."""
        if self.request.method == HTTPMethod.POST:
            return StationSerializerWrite
        return StationSerializerRead

    def post(self, request: Request, save_id: int) -> Response:
        """Create new stations.

        Args:
            request: POST request with the json to create new stations.
            save_id: The ID of the save game the stations belong to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            serializer_class=self.get_serializer_class(),
            data=request.data.get("data"),
            context={"save_id": save_id},
        )

    def get(self, request: Request, save_id: int) -> Response:
        """Get all stations currently configured.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game the stations belong to.

        Returns:
            A JSON response containing a list of stations and their attributes.

        """
        return get_bulk_response(
            request,
            self.get_serializer_class(),
            SaveGame.objects.get(id=save_id).station_set.all(),
        )


class StationView(GenericAPIView):
    """Manage a specific station."""

    serializer_class = StationSerializerRead

    def delete(self, request: Request, save_id: int, id_: int) -> Response:
        """Delete a staion.

        Args:
            request: DELETE Request.
            save_id: The ID of the save game the station belong to.
            id_: The id of the station to delete.

        Returns:
            An empty response if the station been deleted.

        """
        return delete_response(
            Station.objects.filter(
                id=id_,
                game__id=save_id,
                game__user=request.user,
            ),
        )

    def get(self, request: Request, save_id: int, id_: int) -> Response:
        """Get a single sector.

        Args:
            request: GET request.
            save_id: The ID of the save game the station belongs to.
            id_: The ID of the station to get.

        Returns:
            A JSON response for a single station.

        """
        return get_response(
            self.serializer_class,
            Station.objects.filter(
                id=id_,
                game__id=save_id,
                game__user=request.user,
            ),
        )
