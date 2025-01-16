"""Contains the API views for the game portion of the app.

These views allow for the management of  data that is specific to a user or
save game instances context.

"""

from http import HTTPMethod

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.api_bases import X4APIBulkView, X4SingleAPIViewUser
from x4companion.x4.models import Factory, Habitat, SaveGame, Sector, Station
from x4companion.x4.serializers import (
    FactorySerializer,
    HabitatSerializer,
    SaveGameSerializer,
    SectorSerializerRead,
    SectorSerializerWrite,
    StationSerializerRead,
    StationSerializerWrite,
)


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


class SaveGames(X4APIBulkView):
    """Manage save games."""

    serializer_class = SaveGameSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return SaveGame.objects.all()

    def post(self, request: Request, **kwargs) -> Response:
        """Create a new save game.

        Args:
            request: POST request.
            **kwargs: Any kwargs to pass to the endpoint.

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


class SaveGameView(X4SingleAPIViewUser):
    """Manage a single save Game."""

    serializer_class = SaveGameSerializer
    model_class = SaveGame


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
        """Return a QuerySet for getting bulk data."""
        return SaveGame.objects.get(id=kwargs["game_id"]).sector_set.all()


class SectorView(X4SingleAPIViewUser):
    """Manage an individual Sector."""

    serializer_class = SectorSerializerRead

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return Sector.objects.filter(game__user=user, **kwargs)


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
        """Return a QuerySet for getting bulk data."""
        return SaveGame.objects.get(id=kwargs["save_id"]).station_set.all()


class StationView(X4SingleAPIViewUser):
    """Manage a specific station."""

    serializer_class = StationSerializerRead

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return Station.objects.filter(game__user=user, **kwargs)
