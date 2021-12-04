import base64


def username_and_password_to_b64_token(consumer_key, consumer_password, sep: str = ':'):
    return base64.b64encode(f'{consumer_key}:{consumer_password}'.encode()).decode()
