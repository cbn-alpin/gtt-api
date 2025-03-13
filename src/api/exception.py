class DBInsertException(Exception):
    """Exception raised when there is an error inserting data into the database."""

    def __init__(self, message="Error inserting data into database", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(Exception):
    """Exception raised when there is no return."""

    def __init__(self, message="No data found", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class MissingFieldError(Exception):
    """Exception raised when there is missing field."""

    def __init__(self, message="Missing field", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DeleteError(Exception):
    """Exception raised when there is missing field."""

    def __init__(self, message="Missing field", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
