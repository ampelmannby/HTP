import time
import traceback


def decorator(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            e = traceback.format_exc(limit=0)
            print(f'{e}{args}{kwargs}')

    return inner


@decorator
def foo(a, b):
    c = a / b
    print(f'A / B = {c}')


foo(4, 0)

