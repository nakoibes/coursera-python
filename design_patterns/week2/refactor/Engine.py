import Service


class Engine:
    objects = []
    current_knot = 0
    working = True
    show_help = False
    pause = True
    subscribers = set()

    def __init__(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def subscribe_knot(self, knot):
        self.objects.append(knot)

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe_knot(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def notify(self):
        for obj in self.subscribers:
            pass

    def update(self):
        for obj in self.objects:
            obj.update()
            if self.pause is False:
                self.move_points(obj)

    def add_knot(self, obj):
        self.objects.append(obj)

    def del_knot(self, obj):
        self.objects.remove(obj)

    def move_points(self, knot):
        for p in range(len(knot.points)):
            knot.points[p] = knot.points[p] + knot.speeds[p] * knot.speed
            if knot.points[p].int_pair()[0] > self.screen_resolution[0] or knot.points[p].int_pair()[0] < 0:
                knot.speeds[p] = Service.Vec2d(- knot.speeds[p].int_pair()[0], knot.speeds[p].int_pair()[1])
            if knot.points[p].int_pair()[1] > self.screen_resolution[1] or knot.points[p].int_pair()[1] < 0:
                knot.speeds[p] = Service.Vec2d(knot.speeds[p].int_pair()[0], -knot.speeds[p].int_pair()[1])

    def restart(self):
        self.objects = []
