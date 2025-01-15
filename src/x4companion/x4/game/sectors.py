"""Contains API views relating to sectors."""

from http import HTTPMethod

from django.contrib.auth.models import User
from django.db.models import QuerySet

from x4companion.x4.models import SaveGame, Sector
from x4companion.x4.serializers import (
    SectorSerializerRead,
    SectorSerializerWrite,
)
from x4companion.x4.api_bases import X4APIBulkView, X4SingleAPIViewUser


class Sectors(X4APIBulkView):
    """Manage multiple sectors."""

    def get_serializer_class(
        self,
    ) -> type[SectorSerializerRead] | type[SectorSerializerWrite]:
        """Returns correct serializer for the request type."""
        if self.request.method == HTTPMethod.POST:
            return SectorSerializerWrite
        return SectorSerializerRead

    def get_queryset(self, **kwargs) -> QuerySet:
        return SaveGame.objects.get(id=kwargs["game_id"]).sector_set.all()


class SectorView(X4SingleAPIViewUser):
    """Manage an individual Sector."""

    serializer_class = SectorSerializerRead

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        return Sector.objects.filter(game__user=user, **kwargs)
