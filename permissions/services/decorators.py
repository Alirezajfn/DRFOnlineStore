from functools import wraps


def view_permission_codename(name, description=None, group=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.codename = name
        wrapper.description = description
        wrapper.group = group
        return wrapper
    return decorator
