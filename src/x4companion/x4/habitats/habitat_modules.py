"""Contains API views relating to Habitat Modules."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.serializers import HabitatModuleSerializer


class HabitatModules(GenericAPIView):
    """Manage all Habitat Modules."""

    serializer_class = HabitatModuleSerializer

    def post(self, request: Request) -> Response:

        serializer = self.serializer_class(
            data=request.data.get("data"), many=True
        )
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
