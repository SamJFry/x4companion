"""Contains API Views relating to Save Games."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame
from x4companion.x4.serializers import SaveGameSerializer


class SaveGameView(GenericAPIView):
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
            request: Get request.

        Returns:
            Response containing all a users save game.

        """
        serializer = self.serializer_class(SaveGame.objects.all(), many=True)
        return Response(
            {"saves": serializer.data},
            status=status.HTTP_200_OK,
        )
