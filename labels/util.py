from functools import wraps
import json

def retry(retry_times: int = 3):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    print(f"Retry {i + 1}/{retry_times}: {e}")
            return None
        return wrapper
    return decorator


def check_dicts_keys(data, required_keys):
    if isinstance(data, list):
        for d in data:
            if not isinstance(d, dict):
                return False
            if set(d.keys()) != set(required_keys):
                return False
    elif isinstance(data, dict):
        if set(data.keys()) != set(required_keys):
            return False
    else:
        return False
    return True


if __name__ == "__main__":
    @retry(retry_times=7)
    def test(a, b):
        return a / b

    a = test(9, 0)
    print(a)