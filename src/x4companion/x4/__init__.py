from django.http import HttpRequest, JsonResponse

import x4companion


def index(request: HttpRequest) -> JsonResponse:
    """Return some basic information when a user calls the root of the API.

    Args:
        request: The incoming http request.

    Returns:
        JSON response with some information about the app.

    """
    return JsonResponse(
        data={
            "name": "X4 Companion App",
            "version": x4companion.__version__,
        }
    )
