from uuid import UUID


class ApplicationError(Exception):
    pass


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, username: str) -> None:
        super().__init__(f"User '{username}' already exists")


class UsernameCannotBeEmpty(ApplicationError):
    pass


class InvalidCredentialsError(ApplicationError):
    pass


class InvalidTokenError(ApplicationError):
    pass


class TokenExpiredError(ApplicationError):
    pass


class InvalidAdminKeyError(ApplicationError):
    pass


class MasterCardNotFoundError(ApplicationError):
    def __init__(self, card_id: UUID) -> None:
        super().__init__(f"Master card '{card_id}' not found")


class CollectedCardNotFoundError(ApplicationError):
    def __init__(self, card_id: UUID) -> None:
        super().__init__(f"Collected card '{card_id}' not found")
