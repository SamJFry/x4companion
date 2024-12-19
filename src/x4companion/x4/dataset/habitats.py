from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import Habitat, SaveGame, Station
from x4companion.x4.responses import (
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import HabitatSerializer


class StationHabitats(GenericAPIView):
    """Manage all Habitats."""

    serializer_class = HabitatSerializer

    def post(
        self, request: Request, save_id: int, station_id: int
    ) -> Response:
        """Create new Habitats.

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
        """Get all available Habitats for this station.

        Args:
            request: GET request made to this endpoint.
            save_id: The ID of the save game this module belongs to.
            station_id: The ID of the station this module belongs to.

        Returns:
            A JSON response containing a list of Habitats and their
            attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            Station.objects.get(id=station_id).habitat_set.all(),
        )


class StationHabitatsView(GenericAPIView):
    """Manage individual types of habitat on a station."""

    serializer_class = HabitatSerializer

    def get(
        self, request: Request, save_id: int, station_id: int, id_: int
    ) -> Response:
        return get_response(
            self.serializer_class,
            Habitat.objects.filter(
                id=id_,
                station=Station.objects.filter(
                    id=station_id,
                    game=SaveGame.objects.filter(
                        id=save_id, user=request.user
                    ).first(),
                ).first(),
            ),
        )
