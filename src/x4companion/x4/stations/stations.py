"""Contains API views relating to Stations."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import Station
from x4companion.x4.serializers import StationSerializer


class Stations(GenericAPIView):
    """Manage multiple stations."""
    serializer_class = StationSerializer

    def post(self, request: Request, save_id: int):
        data = request.data
        data.update({"user": request.user.id})
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)