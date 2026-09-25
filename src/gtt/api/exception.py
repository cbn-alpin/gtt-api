class APIError(Exception):
    """Base exception for all API business errors."""

    def __init__(
        self,
        message="Une erreur est survenue",
        status_code=400,
        error_type="ERROR",
        error_code="API_ERROR",
    ):
        if isinstance(message, dict) and "message" in message:
            message = message["message"]

        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.error_code = error_code
        super().__init__(self.message)


class DBInsertException(APIError):
    """Exception raised when an error occurs while inserting data into the database."""

    def __init__(self, message="Error inserting data into database"):
        super().__init__(
            message=message,
            status_code=409,
            error_type="DATABASE_ERROR",
            error_code="INSERT_FAILED",
        )


class NotFoundError(APIError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message="Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            error_type="NOT_FOUND",
            error_code="NOT_FOUND",
        )


class MissingFieldError(APIError):
    """Exception raised when a required field is missing from the input data."""

    def __init__(self, message="Missing required field"):
        super().__init__(
            message=message,
            status_code=400,
            error_type="VALIDATION_ERROR",
            error_code="MISSING_FIELD",
        )


class DeleteError(APIError):
    """Exception raised when an error occurs while deleting data."""

    def __init__(self, message="Error deleting data"):
        super().__init__(
            message=message,
            status_code=409,
            error_type="CONFLICT",
            error_code="DELETE_FORBIDDEN",
        )


class UpdateError(APIError):
    """Exception raised when an error occurs while updating data."""

    def __init__(self, message="Error updating data"):
        super().__init__(
            message=message,
            status_code=400,
            error_type="VALIDATION_ERROR",
            error_code="UPDATE_FAILED",
        )
