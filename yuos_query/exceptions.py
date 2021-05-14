class BaseYuosException(Exception):
    pass


class InvalidTokenException(BaseYuosException):
    pass


class InvalidIdException(BaseYuosException):
    pass


class InvalidQueryException(BaseYuosException):
    pass


class InvalidUrlException(BaseYuosException):
    pass
