from django.http import HttpRequest, JsonResponse

import x4companion


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        data={
            "name": "X4 Companion App",
            "version": x4companion.__version__,
        }
    )
