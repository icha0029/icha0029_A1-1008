import abc

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import *

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp
        

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    def get_attack(self, level: int):
        return self.formula_user(self.attack_formula, level)

    def get_defense(self, level: int):
        return self.formula_user(self.defense_formula, level)

    def get_speed(self, level: int):
        return self.formula_user(self.speed_formula, level)

    def get_max_hp(self, level: int):
        return self.formula_user(self.max_hp_formula, level)

    def formula_user(self, formula, level):
        final_stack = ArrayStack(len(formula))
        for levels in formula:
            if levels.isnumeric():
                final_stack.push(float(levels))
            elif levels == "level":
                final_stack.push(level)
            elif levels == "+":
                removed_i = final_stack.pop()
                removed_ii = final_stack.pop()
                final_number = removed_i + removed_ii
                final_stack.push(final_number)
            elif levels == "-":
                removed_i = final_stack.pop()
                removed_ii = final_stack.pop()
                final_number = removed_ii - removed_i
                final_stack.push(final_number)
            elif levels == "*":
                removed_i = final_stack.pop()
                removed_ii = final_stack.pop()
                final_number = removed_ii * removed_i
                final_stack.push(final_number)
            elif levels == "/":
                removed_i = final_stack.pop()
                removed_ii = final_stack.pop()
                final_number = removed_ii / removed_i
                final_stack.push(final_number)
            elif levels == "power":
                removed_i = final_stack.pop()
                removed_ii = final_stack.pop()
                final_number = removed_ii ** removed_i
                final_stack.push(final_number)
            elif levels == "sqrt":
                removed_i = final_stack.pop()
                final_number = removed_i**0.5
                final_stack.push(final_number)
            else: #levels == "middle":
                removed_i = final_stack.pop()
                removed_ii = final_stack.pop()
                removed_iii = final_stack.pop()

                if removed_ii <= removed_i <= removed_iii or removed_iii <= removed_i <= removed_ii:
                    final_stack.push(removed_i)
                if removed_i <= removed_ii <= removed_iii or removed_iii <= removed_ii <= removed_i:
                    final_stack.push(removed_ii)                    
                if removed_i <= removed_iii <= removed_ii or removed_ii <= removed_iii <= removed_i:
                     final_stack.push(removed_iii)                   
        return int(final_stack.pop())

