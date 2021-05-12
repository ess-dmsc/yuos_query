class BaseYuosException(Exception):
    pass


class ConnectionException(BaseYuosException):
    pass


class InvalidIdException(BaseYuosException):
    pass


class InvalidQueryException(BaseYuosException):
    pass
