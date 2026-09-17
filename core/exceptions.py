class ApplicationError(Exception):
    """Base application exception."""


class ConfigurationError(ApplicationError):
    pass


class AuthenticationError(ApplicationError):
    pass


class AuthorizationError(ApplicationError):
    pass


class ToolPermissionError(ApplicationError):
    pass


class DataAccessError(ApplicationError):
    pass


class LLMError(ApplicationError):
    pass


class ValidationError(ApplicationError):
    pass


class HITLRequired(ApplicationError):
    pass