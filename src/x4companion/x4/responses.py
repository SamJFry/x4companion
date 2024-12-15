"""Contains generic responses that can be reused across endpoints."""

from django.db import models
from rest_framework import serializers, status
from rest_framework.response import Response


def delete_response(model: type[models.Model], id_: int, **kwargs) -> Response:
    """Delete a resource from a model.

    Args:
        model: The model the entry belongs to.
        id_: The ID of the DB entry you want to delete.
        **kwargs: Any additional filters to apply to the delete command.

    Returns:
        The DRF response that contains the status.

    """
    deleted = model.objects.filter(id=id_, **kwargs).delete()[0]
    if not deleted:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_response(
    model: type[models.Model],
    serializer: type[serializers.BaseSerializer],
    id_: int,
    **kwargs,
) -> Response:
    """Get a single item from a model.

    Args:
        model: The model the entry belongs to.
        serializer: The serializer used to validate the data.
        id_: The ID of the DB entry you want to delete.
        **kwargs: Any additional filters to apply to the delete command.

    Returns:
        The DRF response that contains the status and result.

    """
    try:
        serializer = serializer(model.objects.get(id=id_, **kwargs))
    except models.ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_response(
    serializer_class: type[serializers.BaseSerializer],
    data: dict,
    context: dict | None = None,
) -> Response:
    """Create DB items from a POST request.

    Args:
        serializer_class: The serializer class to validate the data with.
        data: The data to use to create the DB entries.
        context: Additional context to create the DB entries with.

    Returns:
        The DRF response that contains the status and result.

    """
    serializer = serializer_class(data=data, many=True, context=context)
    if not serializer.is_valid():
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
        )
    try:
        serializer.save()
    except models.ObjectDoesNotExist as e:
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"error": str(e)}
        )
    return Response(status=status.HTTP_201_CREATED, data=serializer.data)
