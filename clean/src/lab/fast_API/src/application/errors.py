class ApplicationError(Exception):
    """Base de todas las excepciones de aplicación."""


class NotFoundError(ApplicationError):
    pass


class ForbiddenError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass


class InvalidCredentialsError(ApplicationError):
    pass
