class MatchingServiceError(Exception):
    """Base exception for matching-service."""


class MatchNotFoundError(MatchingServiceError):
    """Raised when a match suggestion is not found."""


class InvalidMatchError(MatchingServiceError):
    """Raised when a match cannot be created or updated."""


class InvalidMatchDecisionError(MatchingServiceError):
    """Raised when a match decision is invalid."""
