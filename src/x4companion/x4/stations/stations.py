"""Contains API views relating to Stations."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame, Station
from x4companion.x4.serializers import StationSerializerWrite, StationSerializerRead


class Stations(GenericAPIView):
    """Manage multiple stations."""

    def post(self, request: Request, save_id: int) -> Response:
        serializer = StationSerializerWrite(
            data=request.data.get("data"), many=True, context={"save_id": save_id}
        )
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def get(self, request: Request, save_id: int) -> Response:
        game = SaveGame.objects.get(id=save_id)
        serializer = StationSerializerRead(game.station_set.all(), many=True)
        return Response(
            {"stations": serializer.data},
            status=status.HTTP_200_OK,
        )