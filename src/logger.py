from time    import time
from inspect import currentframe

def log_prefix(instance: object, role: str) -> str:
    return "%d:%s.%s[%s].%s" % (
        time(),
        instance.__class__.__module__,
        instance.__class__.__name__,
        role,
        currentframe().f_back.f_code.co_name)

def log_prefix_static(clazz: object, role: str) -> str:
    return "%d:%s.%s[%s].%s" % (
        time(),
        clazz.__module__,
        clazz.__name__,
        role,
        currentframe().f_back.f_code.co_name)
