import Service

class Engine:
    knots = []
    current_knot = 0
    working = True
    show_help = False
    pause = True
    subscribers = set()

    def __init__(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def subscribe_knot(self, knot):
        self.knots.append(knot)

    def subscribe(self,obj):
        self.subscribers.add(obj)

    def unsubscribe_knot(self, knot):
        if knot in self.knots:
            self.knots.remove(knot)

    def notify(self):
        for obj in self.subscribers:
            obj.current_knot = self.current_knot

    def update(self):
        for knot in self.knots:
            knot.knot_points = Service.KnotConstructor(knot.points, knot.steps).get_knot()
            if self.pause is False:
                self.move_points(knot)

    def add_knot(self, knot):
        self.knots.append(knot)

    def del_knot(self, knot):
        self.knots.remove(knot)

    def move_points(self, knot):
        for p in range(len(knot.points)):
            knot.points[p] = knot.points[p] + knot.speeds[p] * knot.speed
            if knot.points[p].int_pair()[0] > self.screen_resolution[0] or knot.points[p].int_pair()[0] < 0:
                knot.speeds[p] = Service.Vec2d(- knot.speeds[p].int_pair()[0], knot.speeds[p].int_pair()[1])
            if knot.points[p].int_pair()[1] > self.screen_resolution[1] or knot.points[p].int_pair()[1] < 0:
                knot.speeds[p] = Service.Vec2d(knot.speeds[p].int_pair()[0], -knot.speeds[p].int_pair()[1])
