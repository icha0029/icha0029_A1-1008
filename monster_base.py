from __future__ import annotations
import abc

from stats import Stats
from elements import *
from math import ceil

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        self.simple_mode = simple_mode
        self.original_level=level
        self.level = level

        if simple_mode:
            self.stats = self.get_simple_stats()
        else:
            self.stats = self.get_complex_stats()

        self.hp = self.get_max_hp()

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        damage_received = self.get_max_hp() - self.get_hp() #Storing damage received by using max hp and minusing current hp
        self.level+=1
        self.set_hp(self.get_max_hp() - damage_received) #Setting new hp by reducing current damage taken so far from new max hp

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.stats.get_attack() #Entering the stats class to get attack data

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.stats.get_defense() #Entering the stats class to get defense data

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.stats.get_speed() #Entering the stats class to get speed data

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.stats.get_max_hp() #Entering the stats class to get max hp 

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.get_hp() > 0

    def dead(self) -> bool:
        """Whether the current monster instance is dead (HP <= 0 )"""
        return self.get_hp() <= 0

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP
        attack = self.get_attack()
        defense = other.get_defense()

        if defense < attack / 2:
            damage = attack - defense

        elif defense < attack:
            damage = attack * 5/8 - defense / 4

        else:
            damage = attack / 4

        element_1 = Element.from_string(self.get_element())
        element_2 = Element.from_string(other.get_element())

        effectiveness = EffectivenessCalculator.get_effectiveness(element_1, element_2)

        effective_damage = ceil(damage * effectiveness)

        other.set_hp(other.get_hp() - effective_damage)



    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        check_1 = self.level > self.original_level # CHecking that the currenr level is higher than the starting level
        check_2 = self.get_evolution() != None #Checking evolution is available
        return check_1 and check_2 

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        damage_received = self.get_max_hp() - self.get_hp() #Storing damage received by using max hp and minusing current hp
        evolved_monster = self.get_evolution()(self.simple_mode , self.get_level()) #Created an instance of the evolved monster
        evolved_monster.set_hp(evolved_monster.get_max_hp() - damage_received) #Setting the damage taken
        return evolved_monster

    def __str__(self):
        return f"LV.{self.get_level()} {self.get_name()}, {self.get_hp()}/{self.get_max_hp()} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

