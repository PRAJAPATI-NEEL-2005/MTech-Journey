class BookException(Exception):
    pass

class ValidationError(BookException):
    pass

class BookNotFoundError(BookException):
    pass

class OutOfStockError(BookException):
    pass
