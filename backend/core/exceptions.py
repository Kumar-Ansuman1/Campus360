class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceNotFoundException(AppException):
    """Raised when a requested resource does not exist."""


class ResourceConflictException(AppException):
    """Raised when a resource conflicts with an existing resource."""


class ResourceValidationException(AppException):
    """Raised when a resource relationship or input is invalid."""


class DatabaseException(AppException):
    """Raised when a database operation fails."""