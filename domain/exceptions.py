class DomainError(Exception):
    """Base error for domain exceptions"""


class ValidationError(DomainError):
    pass


class BusinessRuleError(DomainError):
    pass


class NotFoundError(DomainError):
    pass
