from __future__ import annotations

from enum import auto
from typing import Optional

from base_enum import BaseEnum

from data_structures.referential_array import ArrayR

class Element(BaseEnum):
    """
    Element Class to store all different elements as constants, and associate indicies with them.

    Example:
    ```
    print(Element.FIRE.value)         # 1
    print(Element.GRASS.value)        # 3

    print(Element.from_string("Ice")) # Element.ICE
    ```
    """

    FIRE = auto()
    WATER = auto()
    GRASS = auto()
    BUG = auto()
    DRAGON = auto()
    ELECTRIC = auto()
    FIGHTING = auto()
    FLYING = auto()
    GHOST = auto()
    GROUND = auto()
    ICE = auto()
    NORMAL = auto()
    POISON = auto()
    PSYCHIC = auto()
    ROCK = auto()
    FAIRY = auto()
    DARK = auto()
    STEEL = auto()
    
    """
    Complexity Analysis and Explaination FOR FROM_STRING...
    Which then calculated an index to access the matching effectivness value in the damage_effectiveness_aray and returns it.
    So to start the complexity analysis of from_string can be represented as let g represent the string comparisons.
    Also let p represent the number of iterations. 
    So therefore the best case would be the case in which the first element is string we are searching for so O(G)
    But the worst case would be the case that the last element is the string we are after so its O(G x P) as the loop would rerun P times.
    """
    @classmethod
    def from_string(cls, string: str) -> Element:
        for elem in Element:
            if elem.name.lower() == string.lower():
                return elem
        raise ValueError(f"Unexpected string {string}")



class EffectivenessCalculator:
    """
    Helper class for calculating the element effectiveness for two elements.

    This class follows the singleton pattern.

    Usage:
        EffectivenessCalculator.get_effectiveness(elem1, elem2)
    """

    instance: Optional[EffectivenessCalculator] = None

    def __init__(self, element_names: ArrayR[str], effectiveness_values: ArrayR[float]) -> None:
        """
        Initialise the Effectiveness Calculator.

        The first parameter is an ArrayR of size n containing all element_names.
        The second parameter is an ArrayR of size n*n, containing all effectiveness values.
            The first n values in the array is the effectiveness of the first element
            against all other elements, in the same order as element_names.
            The next n values is the same, but the effectiveness of the second element, and so on.

        Example:
        element_names: ['Fire', 'Water', 'Grass']
        effectivness_values: [0.5, 0.5, 2, 2, 0.5, 0.5, 0.5, 2, 0.5]
        Fire is half effective to Fire and Water, and double effective to Grass [0.5, 0.5, 2]
        Water is double effective to Fire, and half effective to Water and Grass [2, 0.5, 0.5]
        Grass is half effective to Fire and Grass, and double effective to Water [0.5, 2, 0.5]
        
        


        Complexity Analysis and Explanation used for initialisation...
        The effectiveness calculator initializes two arrays elemental_names and damage_effectiveness. 
        These operations are performed in the constant time since they involve assigning values to arrays. 
        Therefore, the best and worst case complexity is 0(1)
        """
        self.elemental_names = element_names
        self.damage_effectiveness = effectiveness_values

    @classmethod
    def get_effectiveness(cls, type1: Element, type2: Element) -> float:
        """
        Returns the effectivness of elem1 attacking elem2.

        Example: EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER) == 0.5


        Complexity Analysis and Explaination...
        FOR GET_EFFECTIVENESS
        Also let p represent the number of loop runs but it also represents the numbers of elements in the array. 
        Also for element comparison represent that as Elem_Comp
        So for best case it would be that the type 1 and type 2 are found first to cut/break of the loop quickly. 
        So the complexity for that would be O(G + Elem_Comp)
        So for worst case it would that the type 1 and type 2 are last to be found in the array
        O(G + Elem_Comp) x O(P)



        """
        index_1 = None
        index_2 = None
        for elemental_index in range(len(cls.instance.elemental_names)): #Iterating through element names
            element = Element.from_string(cls.instance.elemental_names[elemental_index])#Converts into element format
            if index_1 == None and type1 == element: #Checking if index_1 hasn't been asigned a value and type_1 is an element we are after
                index_1 = elemental_index
            if index_2 == None and type2 == element: #Checking if index_2 hasn't been asigned a value and type_2 is an element we are after
                index_2 = elemental_index
            if index_1 != None and index_2 != None: #Breaking if index_1 has a value and index_2 has a value.
                break

        idx_to_search = index_1 * len(cls.instance.elemental_names) + index_2 #Using a formula to get the index from the elemental values 

        return cls.instance.damage_effectiveness[idx_to_search] #Returns damage effectiveness


    @classmethod
    def from_csv(cls, csv_file: str) -> EffectivenessCalculator:
        # NOTE: This is a terrible way to open csv files, if writing your own code use the `csv` module.
        # This is done this way to facilitate the second half of the task, the __init__ definition.
        with open(csv_file, "r") as file:
            header, rest = file.read().strip().split("\n", maxsplit=1)
            header = header.split(",")
            rest = rest.replace("\n", ",").split(",")
            a_header = ArrayR(len(header))
            a_all = ArrayR(len(rest))
            for i in range(len(header)):
                a_header[i] = header[i]
            for i in range(len(rest)):
                a_all[i] = float(rest[i])
            return EffectivenessCalculator(a_header, a_all)

    @classmethod
    def make_singleton(cls):
        cls.instance = EffectivenessCalculator.from_csv("type_effectiveness.csv")

EffectivenessCalculator.make_singleton()


if __name__ == "__main__":
    print(EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER))
