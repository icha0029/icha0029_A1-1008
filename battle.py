from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        #Gets actions for both teams
        action_team_1 = self.team1.choose_action(self.out1, self.out2)
        action_team_2 = self.team2.choose_action(self.out2, self.out1)

        #Completes team 1 action if its not an attack
        if action_team_1 != Battle.Action.ATTACK:
            self.team1.add_to_team(self.out1)
            if action_team_1 == Battle.Action.SPECIAL:
                self.team1.special()
            self.out1 = self.team1.retrieve_from_team()
            team_1_attack = False
        else:
            team_1_attack = True

        #Completes team 2 action if its not an attack
        if action_team_2 != Battle.Action.ATTACK:
            self.team2.add_to_team(self.out2)
            if action_team_2 == Battle.Action.SPECIAL:
                self.team2.special()
            self.out2 = self.team2.retrieve_from_team()
            team_2_attack = False
        else:
            team_2_attack = True

        #Checks if any monsters chose to attack
        if team_1_attack or team_2_attack:
            speed_1 = self.out1.get_speed()
            speed_2 = self.out2.get_speed()

        #checks if monster 1 is faster than monster 2, then monster 1 attacks first. Also monster 2 can retaliate
            if speed_1 > speed_2:
                self.out1.attack(self.out2)
                if self.out2.alive() and team_2_attack:
                    self.out2.attack(self.out1)

        #checks if monster 2 is faster than monster 1, then monster 2 attacks first. Also monster 1 can retaliate
            elif speed_2 > speed_1:
                self.out2.attack(self.out1)
                if self.out1.alive() and team_1_attack:
                    self.out1.attack(self.out2)
        #Both monsters attack each other    
            else:
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)
        #If both monsters after using each others actions and survive then reduce 1 from there hp.
        if self.out1.alive() and self.out2.alive():
            self.out1.set_hp(self.out1.get_hp() - 1)
            self.out2.set_hp(self.out2.get_hp() - 1)

        #checks if both monsters are still alive
        if self.out1.alive() and self.out2.alive():
            return None

        #Does a retreiveing and end of game checks     
        elif self.out1.dead() and self.out2.dead():
            if len(self.team1) > 0:
                if len(self.team2) > 0:
                    self.out1 = self.team1.retrieve_from_team()
                    self.out2 = self.team2.retrieve_from_team()
                else:
                    return self.Result.TEAM1
            else:
                if len(self.team2) > 0:
                    return self.Result.TEAM2
                return self.Result.DRAW
        #Does a retreiveing and end of game checks and evolution check.     
        elif self.out1.alive() and self.out2.dead():
            if len(self.team2) == 0:
                return self.Result.TEAM1
            self.out2 = self.team2.retrieve_from_team()
        

            self.out1.level_up()
            if self.out1.ready_to_evolve():
                self.out1 = self.out1.evolve()

        #Does a retreiveing and end of game checks and evolution check.     
        elif self.out1.dead() and self.out2.alive():
            if len(self.team1) == 0:
                return self.Result.TEAM2
            self.out1 = self.team1.retrieve_from_team()

            self.out2.level_up()
            if self.out2.ready_to_evolve():
                self.out2 = self.out2.evolve()
    


        

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
