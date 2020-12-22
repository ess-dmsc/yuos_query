class BaseYuosSystemException(Exception):
    pass


class ConnectionException(BaseYuosSystemException):
    pass


class InvalidIdException(BaseYuosSystemException):
    pass


class InvalidCredentialsException(BaseYuosSystemException):
    pass
