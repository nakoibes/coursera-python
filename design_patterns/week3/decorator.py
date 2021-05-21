from abc import ABC, abstractmethod


#from hero import Hero


class AbstractEffect(ABC, Hero):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):
    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):

    def get_positive_effects(self):
        tmp = self.base.get_positive_effects()
        tmp.append('Berserk')
        return tmp

    def get_stats(self):
        tmp = self.base.get_stats()
        tmp['Strength'] += 7
        tmp['Luck'] += 7
        tmp['Agility'] += 7
        tmp['Endurance'] += 7
        tmp['Perception'] -= 3
        tmp['Charisma'] -= 3
        tmp['Intelligence'] -= 3
        tmp['HP'] += 50
        return tmp


class Blessing(AbstractPositive):

    def get_positive_effects(self):
        tmp = self.base.get_positive_effects()
        tmp.append('Blessing')
        return tmp

    def get_stats(self):
        tmp = self.base.get_stats()
        tmp['Strength'] += 2
        tmp['Perception'] += 2
        tmp['Endurance'] += 2
        tmp['Charisma'] += 2
        tmp['Intelligence'] += 2
        tmp['Agility'] += 2
        tmp['Luck'] += 2
        return tmp


class Weakness(AbstractNegative):

    def get_negative_effects(self):
        tmp = self.base.get_negative_effects()
        tmp.append('Weakness')
        return tmp

    def get_stats(self):
        tmp = self.base.get_stats()
        tmp['Strength'] -= 4
        tmp['Endurance'] -= 4
        tmp['Agility'] -= 4
        return tmp


class EvilEye(AbstractNegative):

    def get_negative_effects(self):
        tmp = self.base.get_negative_effects()
        tmp.append('EvilEye')
        return tmp

    def get_stats(self):
        tmp = self.base.get_stats()
        tmp['Luck'] -= 10
        return tmp


class Curse(AbstractNegative):

    def get_negative_effects(self):
        tmp = self.base.get_negative_effects()
        tmp.append('Curse')
        return tmp

    def get_stats(self):
        tmp = self.base.get_stats()
        tmp['Strength'] -= 2
        tmp['Perception'] -= 2
        tmp['Endurance'] -= 2
        tmp['Charisma'] -= 2
        tmp['Intelligence'] -= 2
        tmp['Agility'] -= 2
        tmp['Luck'] -= 2
        return tmp
