"""Contains API views relating to Habitat Modules."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import HabitatModule
from x4companion.x4.responses import get_bulk_response, post_response
from x4companion.x4.serializers import HabitatModuleSerializer


class HabitatModules(GenericAPIView):
    """Manage all Habitat Modules."""

    serializer_class = HabitatModuleSerializer

    def post(self, request: Request) -> Response:
        """Create new Habitat Modules.

        Args:
            request: POST request with the json to create new modules.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(self.serializer_class, request.data.get("data"))

    def get(self, request: Request) -> Response:
        """Get all available Habitat Modules.

        Args:
            request: GET request made to this endpoint.

        Returns:
            A JSON response containing a list of Habitat Modules and their
            attributes.

        """
        return get_bulk_response(
            self.serializer_class, HabitatModule.objects.all()
        )
