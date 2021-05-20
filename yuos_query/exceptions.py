class BaseYuosException(Exception):
    pass


class InvalidIdException(BaseYuosException):
    pass


class UnknownInstrumentException(BaseYuosException):
    pass


class ServerException(BaseYuosException):
    pass


class ConnectionException(ServerException):
    pass


class InvalidTokenException(ServerException):
    pass


class InvalidQueryException(ServerException):
    pass


class ImportCacheException(BaseYuosException):
    pass


class ExportCacheException(BaseYuosException):
    pass


class DataUnavailableException(BaseYuosException):
    pass
