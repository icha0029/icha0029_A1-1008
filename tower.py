from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import *

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        self.my_team = None
        self.my_remaining_lifeforce = None
        self.enemy_capacity = None
        self.enemy_teams_stack = None
        """
        As it is self initialisation the best and worse case complexity is O(1)
        """

    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.my_team = team
        self.my_remaining_lifeforce = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)
        """
        This sets my team to the inputted team, and randomly generates the number of lives we have between a min and max value
        best and worse complexity is O(1) for random and and assignment of value of input
        """       

    def generate_teams(self, n: int) -> None:
        self.enemy_capacity = n
        self.enemy_teams_stack = ArrayStack(n)
        for _ in range(n):
            opposing_team = MonsterTeam(team_mode = MonsterTeam.TeamMode.BACK, selection_mode = MonsterTeam.SelectionMode.RANDOM)
            enemy_remaining_lifeforce = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

            opposing_team_tuple = (opposing_team , enemy_remaining_lifeforce)
            self.enemy_teams_stack.push(opposing_team_tuple)
        self.flip_stack(self.enemy_teams_stack)
        """
        I am creating a stack for the required input capacity. 
        The FOR loop creates each enemy teams their amount of lives, then we put it in a tuple.
        and add it to the stack as a tuple so we have both pieces of information together
        Then in the end we flip the stack so its the first item we added.
        So the best and worst case is O(Enemy_Stack) + O(Capacity x (TEAM_Creator)) + O(Capacity) + O(Enemy_Stack) 
                                        = O(Enemy_Stack) + O(Capacity x (TEAM_Creator)), 
                                        team creator = complexity of creating enemy team

        """     

    def battles_remaining(self) -> bool:
        return self.my_remaining_lifeforce > 0 and len(self.enemy_teams_stack) > 0
        """
        This checks if my_team has any lives left and that there are enemy teams left 
        complexity is O(1)
        """


    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        self.my_team.regenerate_team()
        enemy_team, enemy_remaining_lifeforce = self.enemy_teams_stack.pop()
        enemy_team.regenerate_team()
        battle_outcome = self.battle.battle(self.my_team, enemy_team)
        if battle_outcome == Battle.Result.TEAM1:
            enemy_remaining_lifeforce -=1
        elif battle_outcome == Battle.Result.TEAM2:
            self.my_remaining_lifeforce -=1
        else:
            enemy_remaining_lifeforce -=1
            self.my_remaining_lifeforce -=1
        
        self.flip_stack(self.enemy_teams_stack)
        if enemy_remaining_lifeforce > 0:
            self.enemy_teams_stack.push((enemy_team , enemy_remaining_lifeforce))
        self.flip_stack(self.enemy_teams_stack)

        return (battle_outcome , self.my_team , enemy_team , self.my_remaining_lifeforce , enemy_remaining_lifeforce)
        """
        First thing I am doing is regenerating both teams. 
        Which has a complexity of O(Regeneration), Regeneration = complexity

        Next thing we do is battle between my team and enemy time. 
        So the complexity function is O(Fight_Begins), Fight_Begins = complexity of the battle function

        The IF statements have a complexity of O(Final_Comparison), 
        Final_Comparison = complexity of the comparison of battle.result function

        Then I call upon flip stack which has a complexity best and worst case is O(Capacity + Enemy_Stack)

        Then i call upon flip stack again.

        Complexity overall is O(Regeneration) + O(Regeneration) + O(Fight_Begins) + O(Final_Comparison) + O(Capacity + Enemy_Stack) + O(Capacity + Enemy_Stack)
                                = O(Regeneration + Fight_Begins + Final_Comparison + Capacity + Enemy_Stack)
        """

    def out_of_meta(self) -> ArrayR[Element]:
        raise NotImplementedError

    def flip_stack(self, team_stack):
        new_stack = ArrayStack(self.enemy_capacity)
        while len(self.enemy_teams_stack):
            team = team_stack.pop()
            new_stack.push(team)
        self.enemy_teams_stack = new_stack
        """
        This creates a new stack with the required capacity. So the complexity is O(Capacity)
        The WHILE loop runs until we take each elemnt out of the enemy team and add it to a stack 
        so the order is reversed when we are dequeuing the monster at the front
        Complexity of while loop is O(Enemy_Stack), Enemy_Stack = len(self.enemy_teams_stack)
        So overall complexity best and worst case is O(Capacity + Enemy_Stack)
        """     
        


    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)
