from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions import (
    DomainError,
    ValidationError,
    BusinessRuleError,
    NotFoundError,
)


def register_exception_handlers(app):
    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request,
        exc: ValidationError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": "validation_error",
                "message": str(exc),
            },
        )

    @app.exception_handler(BusinessRuleError)
    async def business_rule_error_handler(
        request: Request,
        exc: BusinessRuleError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "error": "business_rule_violation",
                "message": str(exc),
            },
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(
        request: Request,
        exc: NotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "error": "not_found",
                "message": str(exc),
            },
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request,
        exc: DomainError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": "domain_error",
                "message": str(exc),
            },
        )
