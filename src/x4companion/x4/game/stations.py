"""Contains API views relating to Stations."""

from http import HTTPMethod

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SaveGame, Station
from x4companion.x4.responses import (
    delete_response,
    get_response,
)
from x4companion.x4.serializers import (
    StationSerializerRead,
    StationSerializerWrite,
)
from x4companion.x4.api_bases import X4APIBulkView, X4SingleAPIViewUser


class Stations(X4APIBulkView):
    """Manage multiple stations."""

    def get_serializer_class(
        self,
    ) -> type[StationSerializerRead] | type[StationSerializerWrite]:
        """Returns correct serializer for the request type."""
        if self.request.method == HTTPMethod.POST:
            return StationSerializerWrite
        return StationSerializerRead

    def get_queryset(self, **kwargs) -> QuerySet:
        return SaveGame.objects.get(id=kwargs["save_id"]).station_set.all()


class StationView(X4SingleAPIViewUser):
    """Manage a specific station."""

    serializer_class = StationSerializerRead

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        return Station.objects.filter(game__user=user, **kwargs)
