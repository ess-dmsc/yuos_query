class BaseYuosException(Exception):
    pass


class ConnectionException(BaseYuosException):
    pass


class InvalidIdException(BaseYuosException):
    pass


class InvalidCredentialsException(BaseYuosException):
    pass
