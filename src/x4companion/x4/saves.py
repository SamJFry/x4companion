from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.serializers import SaveGameSerializer


class SaveGameView(GenericAPIView):
    serializer_class = SaveGameSerializer

    def post(self, request: Request) -> Response:
        data = request.data
        data.update({"user": request.user.id})
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)