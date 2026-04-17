class AuthServiceError(Exception):
    """Base auth service exception."""


class DuplicateEmailError(AuthServiceError):
    """Raised when the email is already in use."""


class AuthenticationError(AuthServiceError):
    """Raised when credentials are invalid."""


class InactiveUserError(AuthServiceError):
    """Raised when an inactive user attempts to authenticate."""
