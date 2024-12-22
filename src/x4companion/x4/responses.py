"""Contains generic responses that can be reused across endpoints."""

from django.db import models
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response


class BearerTokenAuthentication(TokenAuthentication):
    """Overrides DRFs default token auth to use more standard settings."""

    keyword = "Bearer"


class StandardPaginator(PageNumberPagination):
    """Standard pagination class for all paginated responses."""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


def delete_response(query_set: models.QuerySet) -> Response:
    """Delete a resource from a model.

    Args:
        query_set: The ORM query to use to retrieve the data.

    Returns:
        The DRF response that contains the status.

    """
    if not query_set.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    query_set.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_response(
    serializer: type[serializers.BaseSerializer], query_set: models.QuerySet
) -> Response:
    """Get a single item from a model.

    Args:
        serializer: The serializer used to validate the data.
        query_set: The ORM query to use to retrieve the data.

    Returns:
        The DRF response that contains the status and result.

    """
    if not query_set.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializer(query_set.first())
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


def get_bulk_response(
    request: Request,
    serializer_class: type[serializers.BaseSerializer],
    query_set: models.QuerySet,
) -> Response:
    """Get bulk data from the database.

    Args:
        request: The incoming HTTP request.
        serializer_class: The serializer class to validate the data with.
        query_set: The query set to be used to retrieve the data.

    Returns:
        The DRF response that contains the status and result.
    """
    serializer = serializer_class(query_set, many=True)
    paginator = StandardPaginator()
    data = paginator.paginate_queryset(serializer.data, request)
    if page_size := request.query_params.get(paginator.page_size_query_param):
        paginator.page_size = page_size
    return Response(
        {
            "page": int(paginator.get_page_number(request, paginator)),
            "pages": paginator.page.paginator.num_pages,
            "page_size": int(paginator.page_size),
            "previous": paginator.get_previous_link(),
            "next": paginator.get_next_link(),
            "data": data,
        },
        status=status.HTTP_200_OK,
    )
