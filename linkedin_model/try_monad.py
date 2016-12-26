__author__ = 'yoav'

import inspect

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
            arg_count = 2 if inspect.ismethod(operation) else 1
            if operation.func_code.co_argcount == arg_count:
                success = operation(self.value)
            else:
                success = operation()
            return Success(success)
        except Exception as e:
            return Failure(e)


class Failure(TryLike):
    def __init__(self, exception):
        self.exception = exception

    def map(self, operation):
        return self