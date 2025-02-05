class DBInsertException(Exception):
    """Exception raised when there is an error inserting data into the database."""

    def __init__(self, message="Error inserting data into database", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
