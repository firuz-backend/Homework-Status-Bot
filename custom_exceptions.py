class CustomException(Exception):
    """It is base-class for custom Exceptions."""

    ...


class TokenAvailabilityError(CustomException):
    """The Exception for tokens which were not defined."""

    def __init__(self, message='Не доступен один или несколько из токенов'):
        """Will be send message about error."""
        super().__init__(message)


class EndpointUnavailableError(CustomException):
    """Calls: when API return unexpected status-code."""

    def __init__(self, message):
        """Will be send message about error."""
        super().__init__(message)


class KeysAvailibilityError(CustomException):
    """Calls: when not got expected keys."""

    def __init__(self, message):
        """Will be send message about error."""
        super().__init__(message)


class FormatTypeError(TypeError):
    """It is base-class for custom TypeError-s."""

    ...


class ResponseFormatError(FormatTypeError):
    """Calls: when got unexpected type of object."""

    def __init__(self, message):
        """Will be send message about error."""
        super().__init__(message)


class HomeworksFormatError(FormatTypeError):
    """Calls: when got unexpected type of object."""

    def __init__(self, message):
        """Will be send message about error."""
        super().__init__(message)
