from functools import wraps


def view_permission_codename(name, description=None, group=None):
    """
    Decorator for view function to add codename, description and group
    views decorated with this decorator will be added to
    PermissionPerUrls model when migrations are run
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.codename = name
        wrapper.description = description
        wrapper.group = group
        return wrapper
    return decorator
