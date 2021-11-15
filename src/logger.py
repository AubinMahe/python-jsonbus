from time    import time
from inspect import currentframe

def log_prefix(caller: object, role: str) -> str:
    return "%d:%s.%s[%s].%s" % (
        time(),
        caller.__class__.__module__,
        caller.__class__.__name__,
        role,
        currentframe().f_back.f_code.co_name)
