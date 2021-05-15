class SomeObject:
    def __init__(self):
        self.integer_field = 1
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, type_):
        self.kind = {int: 'int', float: 'float', str: 'str'}[type_]
        self.value = None


class EventSet:
    def __init__(self, value):
        self.kind = {int: 'int', float: 'float', str: 'str'}[type(value)]
        self.value = value


class NullHandler:
    def __init__(self, next_=None):
        self.next = next_

    def handle(self, obj, event):
        if self.next is not None:
            return self.next.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == 'int':
            if event.value is None:
                return obj.integer_field
            else:
                obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == 'float':
            if event.value is None:
                return obj.float_field
            else:
                obj.float_field = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == 'str':
            if event.value is None:
                return obj.string_field
            else:
                obj.string_field = event.value
        else:
            return super().handle(obj, event)

