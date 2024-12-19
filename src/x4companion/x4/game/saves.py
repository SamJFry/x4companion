"""Contains API Views relating to Save Games."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
)
from x4companion.x4.serializers import SaveGameSerializer


class SaveGames(GenericAPIView):
    """Manage save games."""

    serializer_class = SaveGameSerializer

    def post(self, request: Request) -> Response:
        """Create a new save game.

        Args:
            request: POST request.

        Returns:
            A JSON response of the objects created.

        """
        data = request.data
        data.update({"user": request.user.id})
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def get(self, request: Request) -> Response:
        """Get all the save games.

        Args:
            request: GET request.

        Returns:
            Response containing all a users save game.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            SaveGame.objects.all(),
        )


class SaveGameView(GenericAPIView):
    """Manage a single save Game."""

    serializer_class = SaveGameSerializer

    def get(self, request: Request, id_: int) -> Response:
        """Get a save game.

        Args:
            request: GET request.
            id_: Unique ID of the save game.

        Returns:
            Response containing a single save game.

        """
        return get_response(
            self.serializer_class,
            SaveGame.objects.filter(id=id_, user=request.user),
        )

    def delete(self, request: Request, id_: int) -> Response:
        """Delete a save game.

        Args:
            request: DELETE Request.
            id_: Unique ID of the save game to delete.

        Returns:
            Empty response confirming save game has been deleted.

        """
        return delete_response(
            SaveGame.objects.filter(id=id_, user=request.user)
        )
