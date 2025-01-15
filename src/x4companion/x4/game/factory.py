"""Contains Factory views."""

from django.db.models import QuerySet

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import Factory, Station
from x4companion.x4.responses import (
    delete_response,
    get_response,
)
from x4companion.x4.serializers import FactorySerializer
from x4companion.x4.api_bases import X4APIBulkView, X4APISingleView

class StationFactories(X4APIBulkView):
    """Manage all Factories."""

    serializer_class = FactorySerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        return Station.objects.get(id=kwargs["station_id"]).factory_set.all()


class StationFactoriesView(GenericAPIView):
    """Manage individual types of factory on a station."""

    serializer_class = FactorySerializer

    def get(
        self, request: Request, save_id: int, station_id: int, id_: int
    ) -> Response:
        """Get a single factory module associated with a station.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game this module belongs to.
            station_id: The ID of the station this module belongs to.
            id_: The ID of modules.

        Returns:
            A JSON response containing the factory modules.

        """
        return get_response(
            self.serializer_class,
            Factory.objects.filter(
                id=id_,
                station__id=station_id,
                station__game__user=request.user,
                station__game__id=save_id,
            ),
        )

    def delete(
        self, request: Request, save_id: int, station_id: int, id_: int
    ) -> Response:
        """Get a set of factories from a station.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game this module belongs to.
            station_id: The ID of the station this module belongs to.
            id_: The ID of modules.

        Returns:
            An empty response if the modules were deleted.

        """
        return delete_response(
            Factory.objects.filter(
                id=id_,
                station__id=station_id,
                station__game__user=request.user,
                station__game__id=save_id,
            ),
        )
