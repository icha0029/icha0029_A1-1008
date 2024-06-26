from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.array_sorted_list import *
from data_structures.sorted_list_adt import *

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        self.team_mode = team_mode
        if self.team_mode == self.TeamMode.FRONT:
            self.team = ArrayStack(self.TEAM_LIMIT)
        elif self.team_mode == self.TeamMode.BACK:
            self.team = CircularQueue(self.TEAM_LIMIT)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            self.sort_key = kwargs["sort_key"]
            self.descending_checker = True
            self.team = ArraySortedList(self.TEAM_LIMIT)
        else:
            raise ValueError(f"team_mode {self.team_mode} not supported.")

        self.original_team = CircularQueue(self.TEAM_LIMIT)
        self.team_creation_is_completed = False

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
            self.team_creation_is_completed = True
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
            self.team_creation_is_completed = True
        elif selection_mode == self.SelectionMode.PROVIDED:
            provided = kwargs["provided_monsters"]
            if 0 < len(provided) <= self.TEAM_LIMIT:
                for monster in provided:
                    if not monster.can_be_spawned():
                        raise ValueError(f"{monster.get_name()} can't be spawned.")
                self.select_provided(provided)
                self.team_creation_is_completed = True
            else:
                raise ValueError(f"Number of monsters must be within 1 and {self.TEAM_LIMIT}")
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
    """
    Complexity Analysis and Explaination FOR initialisation...
    Initialise is basically initialilsing the team

    Random Mode: the complexity is O(randomise)

    Manual Mode: Overall Complexity is: the while loop is conv + then the printing monsters is O(len(getmonsters x whatevers_inside) + O(TEAM SIZE x (conv + inside)

    Provided Mode: The for loop as we are assuming only valid input so all we are doing is O(p) where p is the length of provided monster.     
        for front: The best and worst complexity is O(p) + O(p) = O(p)
        for back: So the best and worst complexity is O(p) + O(p) = O(p)
        for optimise: The best complexity is O(p) + O(p) = O(p) and worst case case complexity is O(p) + O(p x log(n)) = O(p x log(n))

    """

    def add_to_team(self, monster: MonsterBase):
        if not self.team_creation_is_completed:
            self.original_team.append(type(monster))
        if self.team_mode == self.TeamMode.FRONT:
            self.team.push(monster)
        elif self.team_mode == self.TeamMode.BACK:
            self.team.append(monster)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            if self.SortMode.HP == self.sort_key:
                monster_stat = monster.get_hp()
            elif self.SortMode.ATTACK == self.sort_key:
                monster_stat = monster.get_attack()
            elif self.SortMode.DEFENSE == self.sort_key:
                monster_stat = monster.get_defense()
            elif self.SortMode.SPEED == self.sort_key:
                monster_stat = monster.get_speed()
            elif self.SortMode.LEVEL == self.sort_key:
                monster_stat = monster.get_level()
            monster_item = ListItem(value = monster, key = monster_stat)
            self.team.add(monster_item)
    """
    Complexity Analysis and Explaination FOR ADD_TO_TEAM...
    Add_to_team is basically adding monsters to the team via the choosing of team mode. 

    not_self.team_creation_is completed basically checks that the team has been inititalised.
    If it hasn't then we add the monster to the original team so we can regenerate our monster
    Complexity would've of O(1) from the append but as we do not know the complexity of the 'type' function.
    The best and worst case is O(type)

    For the team mode front I pushed the monster to the front of the stack. 
    Therefore best case complexity and worst case complexity is O(1) as push() gives a complexity of O(1).

    For team mode back I appended which appends the monster to the back of the queue. 
    Therefore best and worst case complexity is O(1) as append() gives a complexity of O(1)

    For team mode optimise we check the if's to get the sorting stats and by using that as the key we put the monster that monster and that sort key (stats) into a list item. 
    That is added to the array sortoed list. Has to be this way as array_sorted_list requires a key to sort the items and also because array sorted list take list item objects. 
    The best complexity of the add function is O(1) because the add function utilised a binary search (middle) to position the new item in the sorted list
    The worst case would then be O(log(n)) where n is the length of the team
    """

    def retrieve_from_team(self) -> MonsterBase:
        if self.team_mode == self.TeamMode.FRONT:
            return self.team.pop()
        elif self.team_mode == self.TeamMode.BACK:
            return self.team.serve()
        elif self.team_mode == self.TeamMode.OPTIMISE:
            if self.descending_checker:
                return self.team.delete_at_index(len(self) - 1).value
            return self.team.delete_at_index(0).value
        """
    Complexity Analysis and Explaination FOR retrieve_from_team...
    retrieve_from_team is basically getting the monster from the team 

    For the team mode front I popped the monster from the front of the stack
    Therefore best case complexity and worst case complexity is O(1) as pop() gives a complexity of O(1).

    For team mode back I served which gets the monster from the front of the queue. 
    Therefore best and worst case complexity is O(1) as serve() gives a complexity of O(1)

    For team mode optimise the delete_at_index function is O(len(self-index)) so the self is team length so when the index is last index its O(1) if the index is at the start O(len(Length of Team))
    """

    def special(self) -> None:
        if self.team_mode == self.TeamMode.FRONT:
            mon_3 = None
            if len(self) > 1:
                mon_1 = self.team.pop()
                mon_2 = self.team.pop()
                if len(self) >= 1:
                    mon_3 = self.team.pop()
                self.team.push(mon_1)
                self.team.push(mon_2)
                if mon_3 != None:
                    self.team.push(mon_3)
        elif self.team_mode == self.TeamMode.BACK:
            storing_queue = CircularQueue(self.TEAM_LIMIT // 2)
            storing_stack = ArrayStack((self.TEAM_LIMIT // 2) + 1)
            max_in_queue = len(self.team) // 2
            monster_count = 0
            while len(self.team):
                monster = self.team.serve()
                if monster_count < max_in_queue:
                    storing_queue.append(monster)
                else:
                    storing_stack.push(monster)
                monster_count += 1
            
            while len(storing_stack):
                monster = storing_stack.pop()
                self.team.append(monster)

            while len(storing_queue):
                monster = storing_queue.serve()
                self.team.append(monster)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            if self.descending_checker:
                self.descending_checker = False
            else:
                self.descending_checker = True
    """
    Complexity Analysis and Explaination FOR special...
    special called some special operations are applied to the team,

    For the team mode front we checked if we had at least 2 monsters.
    Then we took them out and checked if we still had a third monster left.
    If we did then we took it out as well. Then I swtiched the order of monsters to put back in which changes the order of the monsters in the stack.
    Complexity best and worst case is O(1) len, push and pop operations are all O(1) complexity 

    For team mode back for complexity we first create a stack and queue which is O(TEAM_LIMIT). Then I took out a WHILE loop which took out the monsters from the team and added them to the corresponding stack or queue.
    Then we empty out the stack and queue and refill team in required order
    So best and worst case is O(TEAM_LIMIT)

    For team mode optimise its complexity will O(1) as all statements in optimise refer to boolean expressions which are all O(1)
    """


    def regenerate_team(self) -> None:
        while len(self):
            self.retrieve_from_team()

        self.descending_checker = True

        for _ in range(len(self.original_team)):
            monster = self.original_team.serve()
            self.add_to_team(monster())
            self.original_team.append(monster)

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")
    """
    Complexity Analysis and Explaination FOR reg_team...
    reg_team is when we empty the team and refill with new instances of the inital monsters

    For the team mode front the while loop runs n x retrieve so n x 1 so complexity is O(n). 
    The for loop to add monster runs n x new, overall complexity for front is O(n) + O(n x new) which is basically O(n x new)

    For team mode back the while loop runs n x retrieve so n x 1 so complexity is O(n). 
    The for loop to add monster runs n x new, overall complexity for back is O(n) + O(n x new) which is basically O(n x new)

    For team mode optimise the factors are retrieve BC is from the front O(1) and WC is O(n) from the back. for the FOR loop BC is O(1) and WC is O(log(n))
    So overall best case O(n) + O(n x new) 
    So overall worst case is O(n x n) + O(n x log(n) x new)
    """

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        while True:
            team_size = input("Enter Team Size: ") #Requesting Input
            if team_size.isdigit(): #Checking if input can be converted to integer
                team_size = int(team_size)
                if 0 < team_size <= self.TEAM_LIMIT: #Checking if team size is less than 0 and less than the designed limit
                    break
                print(f"Please enter an integer between 1 and {self.TEAM_LIMIT}")
            print("Enter a Number. ")
        
        success = "[✔️]"
        failure = "[❌]"
        print("MONSTERS Are:")
        monster_classes = get_all_monsters()
        for idx, mon in enumerate(monster_classes, start=1):
            if mon.can_be_spawned():
                print(f"{idx}: {mon.get_name()} {success}")
            else:
                print(f"{idx}: {mon.get_name()} {failure}")
        
        for _ in range(team_size):
            while True:
                monster_index = input("Enter the corresponding monster's number: ")
                if monster_index.isdigit():
                    monster_index = int(monster_index) - 1
                    if 0 <= monster_index < len(monster_classes):
                        mon = monster_classes[monster_index]
                        if mon.can_be_spawned(): 
                            self.add_to_team(mon())
                            print(f"{mon.get_name()} was successfully added to the team.")
                            break
                        print("Please Choose A Monster with a [✔️]. ")
                    print(f"Enter a number between 1 and {len(monster_classes)}")
                print("Enter a Number. ")
    """
    Complexity Analysis and Explaination FOR manual...
    manual gets team size and shows possioble monsters for users to spawn and then asks the user for each individual monster they want to spawn.

    While loop to get team size as we are assuming valid input is given the overall complexity is the integer conversion of the string which can be represented as conv. 

    The loop FOR printing_monsters the complexity of get all monsters, so we iterrate over all the monster so the complexity is O(len(getmonsters x whatevers_inside).
    whatevers_inside this contains the can be spawned and get name function. 

    The loop FOR spawning monster this runs 4 times for 4 monster etc. So it runs according users input request for team size therefore complexity O(TEAM SIZE x (conv + inside. 
    inside is: can be spawned, add to team, create new monster instance, get name

    For the team mode front the best and worst case is O(1) 

    For team mode back the best and worst case is O(1)
    
    For team mode optimise the best case is O(1), worst case is log(n)

    Overall Complexity is: the while loop is conv + then the printing monsters is O(len(getmonsters x whatevers_inside) + O(TEAM SIZE x (conv + inside)

    """
                

            
                    
                


    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        
        
        Complexity Analysis and Explaination FOR self_provided...

        self_provided is basically goes for the given array and adds the monsters instance to the team
        length of inputted array = p
        if team mode is __ the complexity
        Front: the add to team method is O(1). Due to the for loop is p times the interior of the for loop. So the best and worst complexity is O(p) as its p x 1 
        Back: the add to team method is O(1). Due to the for loop is p times the interior of the for loop. So the best and worst complexity is O(p) as its p x 1 
        Optimise: the add to team method is O(1). Due to the for loop is p times the interior of the for loop. So the best complexity is O(p) as its p x 1.
        and the worst case is p x log(n) n same as before defintion
        """
        for monster in provided_monsters:
            self.add_to_team(monster())

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

    def __len__(self):
        return len(self.team)

    """ 
    Complexity is O(1)
    """

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())

