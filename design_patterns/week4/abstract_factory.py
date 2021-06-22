import random


class AbstractLevel:
    @classmethod
    def get_map(cls):
        return cls.Map()

    @classmethod
    def get_objects(cls):
        return cls.Objects()


class EasyLevel(AbstractLevel):
    class Map:

        def __init__(self):
            self._map = [[0 for j in range(5)] for i in range(5)]
            for i in range(5):
                for j in range(5):
                    if i == 0 or j == 0 or i == 4 or j == 4:
                        self._map[j][i] = -1
                    else:
                        self._map[j][i] = random.randint(0, 2)

        def get_map(self):
            return self._map

    class Objects:

        def __init__(self):
            self.objects = [('next_lvl', (2, 2))]

        def get_objects(self, map_obj):
            # размещаем противников
            for obj_name in ['rat']:
                coord = (random.randint(1, 3), random.randint(1, 3))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 3), random.randint(1, 3))

                self.objects.append((obj_name, coord))

            return self.objects


class MediumLevel(AbstractLevel):
    class Map:

        def __init__(self):
            self._map = [[0 for j in range(8)] for i in range(8)]
            for i in range(8):
                for j in range(8):
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        self._map[j][i] = -1
                    else:
                        self._map[j][i] = random.randint(0, 2)

        def get_map(self):
            return self._map

    class Objects:

        def __init__(self):
            self.objects = [('next_lvl', (4, 4))]

        def get_objects(self, map_obj):
            for obj_name in ['rat', 'snake']:
                coord = (random.randint(1, 6), random.randint(1, 6))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 6), random.randint(1, 6))

                self.objects.append((obj_name, coord))

            return self.objects


class HardLevel(AbstractLevel):
    class Map:

        def __init__(self):
            self._map = [[0 for j in range(10)] for i in range(10)]
            for i in range(10):
                for j in range(10):
                    if i == 0 or j == 0 or i == 9 or j == 9:
                        self._map[j][i] = -1
                    else:
                        self._map[j][i] = random.randint(-1, 8)

        def get_map(self):
            return self._map

    class Objects:

        def __init__(self):
            self.objects = [('next_lvl', (5, 5))]

        def get_objects(self, map_obj):
            for obj_name in ['rat', 'snake']:
                coord = (random.randint(1, 8), random.randint(1, 8))
                intersect = True
                while intersect:
                    intersect = False
                    if map_obj[coord[0]][coord[1]] == -1:
                        intersect = True
                        coord = (random.randint(1, 8), random.randint(1, 8))
                        continue
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 8), random.randint(1, 8))

                self.objects.append((obj_name, coord))

            return self.objects
