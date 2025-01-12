"""Contains Factory views."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import Factory, Station
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import FactorySerializer


class StationFactories(GenericAPIView):
    """Manage all Factories."""

    serializer_class = FactorySerializer

    def post(
        self, request: Request, save_id: int, station_id: int
    ) -> Response:
        """Create new Factories.

        Args:
            request: POST request with the json to create new modules.
            save_id: The ID of the save game this module belongs to.
            station_id: The ID of the station this module belongs to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            self.serializer_class,
            request.data.get("data"),
            context={"save_id": save_id, "station_id": station_id},
        )

    def get(self, request: Request, save_id: int, station_id: int) -> Response:
        """Get all available Factories for this station.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game this module belongs to.
            station_id: The ID of the station this module belongs to.

        Returns:
            A JSON response containing a list of Factories and their
            attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            Station.objects.get(id=station_id).factory_set.all(),
        )


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
