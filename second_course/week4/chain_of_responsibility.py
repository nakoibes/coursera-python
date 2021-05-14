class SomeObject:
    def __init__(self):
        self.integer_field = 1
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, type_):
        self.type = type_


class EventSet:
    def __init__(self, value):
        self.value = value


class NullHandler:
    def __init__(self, next_=None):
        self.next = next_

    def handle(self, obj, event):
        if self.next is not None:
            return self.next.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == int:
            return obj.integer_field
        elif isinstance(event, EventSet) and isinstance(event.value, int):
            obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == float:
            return obj.float_field
        elif isinstance(event, EventSet) and isinstance(event.value, float):
            obj.float_field = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == str:
            return obj.string_field
        elif isinstance(event, EventSet) and isinstance(event.value, str):
            obj.string_field = event.value
        else:
            return super().handle(obj, event)


