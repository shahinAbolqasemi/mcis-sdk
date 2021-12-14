import base64
import inspect


def get_default_args(func: callable) -> dict:
    return {
        k: v.default
        for k, v
        in inspect.signature(func).parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def username_and_password_to_b64_token(consumer_key, consumer_password, sep: str = ':'):
    return base64.b64encode(f'{consumer_key}:{consumer_password}'.encode()).decode()
