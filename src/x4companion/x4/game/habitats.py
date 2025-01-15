"""Contains Habitat views."""
from django.contrib.auth.models import User
from django.db.models import QuerySet

from x4companion.x4.models import Habitat, Station
from x4companion.x4.serializers import HabitatSerializer
from x4companion.x4.api_bases import X4APIBulkView, X4SingleAPIViewUser


class StationHabitats(X4APIBulkView):
    """Manage all Habitats."""

    serializer_class = HabitatSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return Station.objects.get(id=kwargs["station_id"]).habitat_set.all()


class StationHabitatsView(X4SingleAPIViewUser):
    """Manage individual types of habitat on a station."""

    serializer_class = HabitatSerializer

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return Habitat.objects.filter(station__game__user=user, **kwargs)
