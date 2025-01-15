"""Contains templates for the Apps API views."""
from typing import Type

from django.db.models import QuerySet, Model
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)


class X4APIBulkView(APIView):
    """API View for managing bulk data."""

    serializer_class: Type[BaseSerializer]
    model_class: Type[Model]

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting bulk data."""
        return self.model_class.objects.filter(**kwargs)

    def post(self, request: Request, **kwargs) -> Response:
        """Create an API resource.

        Args:
            request: The incoming HTTP request.
            **kwargs: Arguments to pass to the Serializers context.

        Returns:
            A JSON response with the created objects.

        """
        return post_response(
            self.serializer_class,
            request.data.get("data"),
            context=kwargs,
        )

    def get(self, request: Request, **kwargs) -> Response:
        """Return bulk API resources that exist in the database.

        Args:
            request: The incoming HTTP request.
            **kwargs: Arguments to pass to the queryset.

        Returns:
            A JSON response with all matching objects.

        """
        return get_bulk_response(
            request,
            self.serializer_class,
            self.get_queryset(**kwargs),
        )


class X4APISingleView(APIView):
    """API view for managing singular data."""

    serializer_class: Type[BaseSerializer]
    model_class: Type[Model]

    def get_queryset(self, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return self.model_class.objects.filter(**kwargs)

    def get(self, request: Request, **kwargs) -> Response:
        """Get a single API object by its ID.

        Args:
            request: The incoming HTTP request.
            **kwargs: Arguments to pass to the queryset.

        Returns:
            A JSON response with the matching object.

        """
        return get_response(self.serializer_class, self.get_queryset(**kwargs))

    def delete(self, request: Request, **kwargs) -> Response:
        """Delete an API object by its ID.

        Args:
            request: The incoming HTTP request.
            **kwargs: Arguments to pass to the queryset.

        Returns:
            An empty 204 response.

        """
        return delete_response(self.get_queryset(**kwargs))
