"""Contains API views relating to Factory Modules."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import FactoryModule
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import FactoryModuleSerializer


class FactoryModules(GenericAPIView):
    """Manage all Factory Modules."""

    serializer_class = FactoryModuleSerializer

    def post(self, request: Request, dataset_id: int) -> Response:
        """Create new Factory Modules.

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
        """Get all available Factory Modules.

        Args:
            request: GET request made to this endpoint.
            dataset_id: The dataset you want to retrieve modules from.

        Returns:
            A JSON response containing a list of Factory Modules and their
            attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            FactoryModule.objects.filter(dataset=dataset_id),
        )


class FactoryModuleView(GenericAPIView):
    """Manage an individual Factory Module."""

    serializer_class = FactoryModuleSerializer

    def get(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Get a Factory Module.

        Args:
            request: The incoming GET request.
            dataset_id: The ID of the dataset the module belongs to.
            id_: The ID of the Module.

        Returns:
            A JSON Response containing the requested Module.

        """
        return get_response(
            self.serializer_class,
            FactoryModule.objects.filter(id=id_, dataset=dataset_id),
        )

    def delete(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Delete a Factory Module.

        Args:
            request: The incoming DELETE request.
            dataset_id: The dataset the module belongs to.
            id_: The ID of the Module.

        Returns:
            An empty response if the module has been deleted.

        """
        return delete_response(
            FactoryModule.objects.filter(id=id_, dataset=dataset_id)
        )
