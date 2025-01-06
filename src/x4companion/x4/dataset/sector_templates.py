"""Contains views for Sector Templates."""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from x4companion.x4.models import SectorTemplate
from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)
from x4companion.x4.serializers import SectorTemplateSerializer


class SectorTemplates(GenericAPIView):
    """Manage sector templates for a dataset."""

    serializer_class = SectorTemplateSerializer

    def post(self, request: Request, dataset_id: int) -> Response:
        """Create new Sector Templates.

        Args:
            request: POST request with the json to create new templates.
            dataset_id: The dataset you want to add the template to.

        Returns:
            JSON Response detailing the objects that have been created.

        """
        return post_response(
            self.serializer_class,
            request.data.get("data"),
            context={"dataset_id": dataset_id},
        )

    def get(self, request: Request, dataset_id: int) -> Response:
        """Get all available Sector Templates in the Dataset.

        Args:
            request: GET request made to this endpoint.
            dataset_id: The dataset you want to retrieve templates from.

        Returns:
            A JSON response containing a list of Sector Templates and their
            attributes.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            SectorTemplate.objects.filter(dataset=dataset_id),
        )


class SectorTemplatesView(GenericAPIView):
    """Manage an individual sector template."""

    serializer_class = SectorTemplateSerializer

    def get(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Get a Sector Template.

        Args:
            request: The incoming GET request.
            dataset_id: The ID of the dataset the template belongs to.
            id_: The ID of the template.

        Returns:
            A JSON Response containing the requested template.

        """
        return get_response(
            self.serializer_class,
            SectorTemplate.objects.filter(id=id_, dataset=dataset_id),
        )

    def delete(self, request: Request, dataset_id: int, id_: int) -> Response:
        """Delete a Sector Template.

        Args:
            request: The incoming DELETE request.
            dataset_id: The dataset the template belongs to.
            id_: The ID of the template.

        Returns:
            An empty response if the template has been deleted.

        """
        return delete_response(
            SectorTemplate.objects.filter(id=id_, dataset=dataset_id)
        )
