from functools import wraps


def view_permission_codename(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.codename = name
        return wrapper
    return decorator
