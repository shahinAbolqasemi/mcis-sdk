import functools
from mci_services.utils import get_default_args


def request_url(url: str):
    def decorator(func: callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            default_args = None
            while True:
                try:
                    formatted_url = url.format(**kwargs)
                    break
                except KeyError as ex:
                    not_founded_key = ex.args[0]
                    default_args = default_args or get_default_args(func)
                    kwargs[not_founded_key] = default_args[not_founded_key]
            return func(*args, **kwargs, url=formatted_url)

        return wrapper

    return decorator
