__author__ = 'yoav'


class Try(object):
    def __new__(self,operation):
        try:
            return Success(operation()) if callable(operation) else Success(operation)
        except Exception as e:
            return Failure(e)


class TryLike(object):
    def map(self, operation):
        try:
            value = operation()
            return Success(value)
        except Exception as e:
            return Failure(e)
        pass
    def isSuccess(self):
        return isinstance(self, Success)

    def isFailure(self):
        return isinstance(self, Failure)


class Success(TryLike):

    def __init__(self, value):
        self.value = value

    def map(self, operation):
        try:
            success = operation(self.value)
            return Success(success)
        except Exception as e:
            return Failure(e)


class Failure(TryLike):
    def __init__(self, exception):
        self.exception = exception

    def map(self, operation):
        return self