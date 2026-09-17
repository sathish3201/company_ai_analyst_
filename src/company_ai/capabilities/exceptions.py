class CapabilityError(Exception):
    """
    Base capability exception.
    """


class CapabilityRegistrationError(
    CapabilityError
):
    """
    Raised when capability registration fails.
    """


class CapabilityNotFoundError(
    CapabilityError
):
    """
    Raised when a capability cannot be resolved.
    """


class CapabilityExecutionError(
    CapabilityError
):
    """
    Raised when capability execution fails.
    """