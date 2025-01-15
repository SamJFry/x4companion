"""Contains Factory views."""

from django.contrib.auth.models import User
from django.db.models import QuerySet

from x4companion.x4.models import Factory, Station
from x4companion.x4.serializers import FactorySerializer
from x4companion.x4.api_bases import X4APIBulkView, X4SingleAPIViewUser

class StationFactories(X4APIBulkView):
    """Manage all Factories."""

    serializer_class = FactorySerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return Station.objects.get(id=kwargs["station_id"]).factory_set.all()


class StationFactoriesView(X4SingleAPIViewUser):
    """Manage individual types of factory on a station."""

    serializer_class = FactorySerializer

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return Factory.objects.filter(station__game__user=user, **kwargs)
