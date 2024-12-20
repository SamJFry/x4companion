"""Contains API views relating to sectors."""

from http import HTTPMethod

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame, Sector
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import (
    SectorSerializerRead,
    SectorSerializerWrite,
)


class Sectors(GenericAPIView):
    """Manage multiple sectors."""

    def get_serializer_class(
        self,
    ) -> type[SectorSerializerRead] | type[SectorSerializerWrite]:
        """Returns correct serializer for the request type."""
        if self.request.method == HTTPMethod.POST:
            return SectorSerializerWrite
        return SectorSerializerRead

    def get(self, request: Request, save_id: int) -> Response:
        """Get all sectors currently configured.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game the sectors belong to.

        Returns:
            A JSON response containing a list of sectors and their attributes.

        """
        return get_bulk_response(
            request,
            self.get_serializer_class(),
            SaveGame.objects.get(id=save_id).sector_set.all(),
        )

    def post(self, request: Request, save_id: int) -> Response:
        """Creates a new sector in the database.

        Args:
            request: POST request with the json to create a new sector.
            save_id: The ID of the save game the sectors belong to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            serializer_class=self.get_serializer_class(),
            data=request.data.get("data"),
            context={"game_id": save_id},
        )


class SectorView(GenericAPIView):
    """Manage an individual Sector."""

    serializer_class = SectorSerializerRead

    def get(self, request: Request, save_id: int, id_: int) -> Response:
        """Get a single sector.

        Args:
            request: GET request.
            save_id: The ID of the save game the sector belongs to.
            id_: The ID of the sector to get.

        Returns:
            A JSON response for a single sector.

        """
        return get_response(
            serializer=self.serializer_class,
            query_set=Sector.objects.filter(
                id=id_,
                game__id=save_id,
                game__user=request.user,
            ),
        )

    def delete(self, request: Request, save_id: int, id_: int) -> Response:
        """Delete a sector from the Database.

        Args:
            request: DELETE Request.
            save_id: The ID of the save game the sector belong to.
            id_: The id of the sector to delete.

        Returns:
            An empty response if the sector has been deleted.

        """
        return delete_response(
            Sector.objects.filter(
                id=id_,
                game__id=save_id,
                game__user=request.user,
            )
        )
