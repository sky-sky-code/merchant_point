class Route:
    def __init__(self, point, func, **kwargs):
        self.point = point
        self.func = func
        self.kwargs = kwargs

    def handle(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Router:

    def __init__(self):
        self.route = []

    def __call__(self, *args, **kwargs):
        for route in self.route:
            if route.point == kwargs['point']:
                return route.handle(*args, **kwargs)

    def add_route(self, point, func, **kwargs):
        route = Route(point, func, **kwargs)
        self.route.append(route)


class App:
    def __init__(self):
        self.router = Router()

    def __call__(self, *args, **kwargs):
        return self.router(*args, **kwargs)

    def route(self, point, **kwargs):
        def decorator(func):
            self.router.add_route(point, func, **kwargs)
            return func
        return decorator
