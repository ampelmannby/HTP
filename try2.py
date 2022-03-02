import traceback


class Market:
    def __init__(self, market):
        self.symbol = market


class NonStop():
    def __init__(self, a, b, q):
        self.a = a
        self.b = b
        self.q = q

    def non_stop(self, func):
        try:
            func()
        except Exception:
            e = traceback.format_exc(limit=0)
            print(f'{e}{self.a=}\n{self.b=}')

    def foo(self):
        c = self.a / self.b
        print(f'A / B = {c}')
        print(self.q.symbol)

    def start(self):
        self.non_stop(self.foo)


def bar(x, y, market):
    q = Market(market)
    z = NonStop(x, y, q)

    z.start()



for i in range(10):
    print(f"\nIteration #{i}")
    bar(i, i % 2, 'US30')
