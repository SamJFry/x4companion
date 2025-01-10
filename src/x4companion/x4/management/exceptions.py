"""Exceptions for management commands in the x4 module."""

from rest_framework.serializers import ErrorDetail


class ObjectExistsError(Exception):
    """Raised for a validation error with the unique error code."""

    def __init__(self) -> None:
        msg = "Dataset with specified name already exists."
        super().__init__(msg)


class ValidationError(Exception):
    """Generic error raised for serializer errors.

    Args:
        errors: The dictionary of errors from a DRF serializer.

    """

    def __init__(
        self,
        errors: list[dict[str, list[ErrorDetail]]]
        | dict[str, list[ErrorDetail]],
    ) -> None:
        name_error = None if isinstance(errors, list) else errors.get("name")
        if (
            name_error
            and len(name_error) == 1
            and name_error[0].code == "unique"
        ):
            raise ObjectExistsError
        super().__init__(errors)
