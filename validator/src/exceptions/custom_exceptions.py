class AppError(Exception):
    pass

class ValidationError(AppError):
    pass

class SchemaError(AppError):
    pass

class ParserError(AppError):
    pass

class MissingFieldError(ValidationError):
    pass

class TypeMismatchError(ValidationError):
    pass

class ConstraintError(ValidationError):
    pass