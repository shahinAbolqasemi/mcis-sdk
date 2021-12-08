import functools


def request_url(url: str):
    def decorator(func: callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            formatted_url = url.format(**kwargs)
            return func(*args, **kwargs, url=formatted_url)

        return wrapper

    return decorator
