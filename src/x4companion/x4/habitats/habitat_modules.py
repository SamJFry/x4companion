"""Contains API views relating to Habitat Modules."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.serializers import HabitatModuleSerializer
from x4companion.x4.responses import post_response


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
