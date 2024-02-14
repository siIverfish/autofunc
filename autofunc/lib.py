import inspect

SENTINEL = object()

class SignedFunction:
    def __init__(self, function, proxy=None):
        self.f = function

        try:
            self.signature = inspect.signature(proxy or function)
        except ValueError as e:
            print(f"Attempted to call `SignedFunction` on builtin function {function.__name__}."+\
                   "Use `proxy` argument instead.")
            raise e
    
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


class AutoFunction:
    def __init__(self, function):
        self.function = function

        self.args = []
        self.kwargs = {}

    def _ingest_item(self, value, key=None):
        # print(f"AutoFunction.__call__({self.function.f.__name__}, {value}) -- args {self.args}, kwargs {self.kwargs}")
        
        # recurse case: have the rightmost child AutoFunction ingest this argument instead of this one.
        # eventually it will be "full" and replace itself with an output value.
        if self.args and isinstance(self.args[-1], AutoFunction | AutoFunctionFactory):
            # smooth over AutoFunctionFactory inconsistencies -- refactor ?
            if isinstance(self.args[-1], AutoFunctionFactory):
                self.args[-1] = self.args[-1]._new_child()
            self.args[-1] = self.args[-1]._ingest_item(value, key)
        else:
        # base case: this class ingests the argument, settings args/kwargs
            if key is None:
                self.args.append(value)
            else:
                if self.kwargs.get(key, SENTINEL) is not SENTINEL:
                    raise ValueError(f"key {key} already in keyword arguments")
                self.kwargs[key] = value

        # if this class is now "full" (has all required arguments)
        # return the result instead of `self`
        if len(self.args) + len(self.kwargs) == len(self.function.signature.parameters) and \
            not any(isinstance(x, AutoFunction | AutoFunctionFactory) for x in self.args):
            return self.function(*self.args, **self.kwargs)
        else:
            return self

    def __call__(self, *args, **kwargs):
        value = self
        for value in args:
            value = self._ingest_item(value)
        for key, value in kwargs.items():
            value = self._ingest_item(value, key)
        return value


class AutoFunctionFactory:
    def __init__(self, function):
        if not isinstance(function, SignedFunction):
            raise TypeError(f"AutoFunctionFactory.__init__ takes SignedFunction instance, not {function.__class__}")
        
        self.function = function
        self.f = self.function.f
    
    def _new_child(self):
        return AutoFunction(self.function)

    def __call__(self, *args, **kwargs):
        return self._new_child()(*args, **kwargs)


def auto(func, proxy=None):
    return AutoFunctionFactory(SignedFunction(func, proxy))


__all__ = ["auto"]