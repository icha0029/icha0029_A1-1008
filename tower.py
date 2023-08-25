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

    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.my_team = team
        self.my_remaining_lifeforce = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_teams(self, n: int) -> None:
        self.enemy_capacity = n
        self.enemy_teams_stack = ArrayStack(n)
        for _ in range(n):
            opposing_team = MonsterTeam(team_mode = MonsterTeam.TeamMode.BACK, selection_mode = MonsterTeam.SelectionMode.RANDOM)
            enemy_remaining_lifeforce = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

            opposing_team_tuple = (opposing_team , enemy_remaining_lifeforce)
            self.enemy_teams_stack.push(opposing_team_tuple)
        self.flip_stack(self.enemy_teams_stack)

    def battles_remaining(self) -> bool:
        return self.my_remaining_lifeforce > 0 and len(self.enemy_teams_stack) > 0


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

    def out_of_meta(self) -> ArrayR[Element]:
        raise NotImplementedError

    def flip_stack(self, team_stack):
        new_stack = ArrayStack(self.enemy_capacity)
        while len(self.enemy_teams_stack):
            team = team_stack.pop()
            new_stack.push(team)
        self.enemy_teams_stack = new_stack
        


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
