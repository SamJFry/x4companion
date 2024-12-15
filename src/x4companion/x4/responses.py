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
        The DRF response that contains the status.

    """
    try:
        serializer = serializer(model.objects.get(id=id_, **kwargs))
    except models.ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)
