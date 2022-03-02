import traceback


class Number:
    a = int()
    b = int()


num = 0


def non_stop(func):

    try:
        func(num.a, num.b)
    except Exception:
        e = traceback.format_exc(limit=0)
        print(f'{e}{num.a=}\n{num.b=}')


def foo(a, b):
    c = a / b
    print(f'A / B = {c}')


def start(a, b):
    global num
    num = Number()
    num.a = a
    num.b = b
    @non_stop
    def bar(a, b):
        foo(num.a, num.b)
    return

start(4, 5)

