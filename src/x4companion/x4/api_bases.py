"""Contains templates for the Apps API views."""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from x4companion.x4.responses import (
    delete_response,
    get_bulk_response,
    get_response,
    post_response,
)


class X4APIBulkView(APIView):
    """API View for managing bulk data."""

    serializer_class: type[BaseSerializer]
    model_class: type[Model]

    def get_serializer_class(self) -> type[BaseSerializer]:
        """Default method to return a serializer class."""
        return self.serializer_class

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
            self.get_serializer_class(),
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
        try:
            return get_bulk_response(
                request,
                self.get_serializer_class(),
                self.get_queryset(**kwargs),
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class X4APISingleView(APIView):
    """API view for managing singular data."""

    serializer_class: type[BaseSerializer]
    model_class: type[Model]

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


class X4SingleAPIViewUser(X4APISingleView):
    """Passes a user instance in addition to the kwargs in it's queryset.

    The class is otherwise identical to its parent. It should be used in
    instances where you want to restrict the returned objects to just those
    that are associated with the user.

    """

    def get_queryset(self, user: User, **kwargs) -> QuerySet:
        """Return a QuerySet for getting a single item."""
        return self.model_class.objects.filter(user=user, **kwargs)

    def get(self, request: Request, **kwargs) -> Response:
        """Get a single API object by its ID.

        Args:
            request: The incoming HTTP request.
            **kwargs: Arguments to pass to the queryset.

        Returns:
            A JSON response with the matching object.

        """
        return get_response(
            self.serializer_class, self.get_queryset(request.user, **kwargs)
        )

    def delete(self, request: Request, **kwargs) -> Response:
        """Delete an API object by its ID.

        Args:
            request: The incoming HTTP request.
            **kwargs: Arguments to pass to the queryset.

        Returns:
            An empty 204 response.

        """
        return delete_response(self.get_queryset(request.user, **kwargs))
