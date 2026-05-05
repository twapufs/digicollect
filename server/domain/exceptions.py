class DomainError(Exception):
    pass


class CardNotAvailableError(DomainError):
    pass


class InvalidQuantityError(DomainError):
    pass


class InsufficientPermissionsError(DomainError):
    pass
