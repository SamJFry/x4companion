"""Contains API views relating to Habitat Modules."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import HabitatModule
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import HabitatModuleSerializer


class HabitatModules(GenericAPIView):
    """Manage all Habitat Modules."""

    serializer_class = HabitatModuleSerializer

    def post(self, request: Request, dataset_id: int) -> Response:
        """Create new Habitat Modules.

        Args:
            request: POST request with the json to create new modules.
            dataset_id: The dataset you want to add the module to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            self.serializer_class,
            request.data.get("data"),
            context={"dataset_id": dataset_id},
        )

    def get(self, request: Request, dataset_id: int) -> Response:
        """Get all available Habitat Modules.

        Args:
            request: GET request made to this endpoint.
            dataset_id: The dataset you want to add the module to.

        Returns:
            A JSON response containing a list of Habitat Modules and their
            attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            HabitatModule.objects.filter(dataset=dataset_id),
        )


class HabitatModuleView(GenericAPIView):
    """Manage an individual Habitat Module."""

    serializer_class = HabitatModuleSerializer

    def get(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Get a Habitat Module.

        Args:
            request: The incoming GET request.
            dataset_id: The ID of the dataset the module belongs to.
            id_: The ID of the Module.

        Returns:
            A JSON Response containing the requested Module.

        """
        return get_response(
            HabitatModule, self.serializer_class, id_, dataset=dataset_id
        )

    def delete(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Delete a Habitat Module.

        Args:
            request: The incoming DELETE request.
            dataset_id: The dataset the module belongs to.
            id_: The ID of the Module.

        Returns:
            An empty response if the module has been deleted.

        """
        return delete_response(HabitatModule, id_, dataset=dataset_id)
