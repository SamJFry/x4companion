class DatasetExistsError(Exception):
    def __init__(self):
        msg = "Dataset with specified name already exists."
        super().__init__(msg)


class ValidationError(Exception):
    def __init__(self, errors):
        name_error = errors.get("name")
        if (
            name_error
            and len(name_error) == 1
            and name_error[0].code == "unique"
        ):
            raise DatasetExistsError
        super().__init__(errors)
