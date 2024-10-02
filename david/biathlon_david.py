import random
from enum import Enum
from typing import List

TypeMatchingDict = {
    "1":"１",
    "2":"２",
    "3":"３",
    "4":"４",
    "5":"５"
    }

class player_state(Enum):
    EPS_HasSpoon = 0
    EPS_NotHasSpoon = 1

class wrong_input(Exception):
    pass

class name_taken(Exception):
    pass
    
class player():
    PlayerNames: List[str] = []
    def __init__(self, playerName):
        self.playerName = playerName
        self.playerState = player_state.EPS_NotHasSpoon
        self.playerNumber = len(player.PlayerNames)
        player.PlayerNames.append(playerName)
        self.targetsDict = {
            "１":"◯",
            "２":"◯",
            "３":"◯",
            "４":"◯",
            "５":"◯"
            }
        self.remainingRounds = 5
        self.scoreBoard = score_board()
    def give_spoon(self):
        self.playerState = player_state.EPS_HasSpoon
    def take_spoon(self):
        self.playerState = player_state.EPS_NotHasSpoon
        self.remainingRounds-=1
    def load_TargetDict(self):
        print(" ".join(self.targetsDict.keys()))
        print(" ".join(self.targetsDict.values()))
    def shoot(self, player_input):
        hit_or_miss = random.choice(["◯", "⭐"])
        if hit_or_miss == "◯":
            print("\nMiss")
            return
        elif self.targetsDict[TypeMatchingDict[player_input]] == "◯":
            print("\nHit on open target")
            self.scoreBoard.add_to_score()
            self.targetsDict[TypeMatchingDict[player_input]] = hit_or_miss
            return
        elif self.targetsDict[TypeMatchingDict[player_input]] == "⭐":
            print("\nHit on closed target")
            return
    
    
class score_board():
    def __init__(self):
        self.currentScore = 0
    def add_to_score(self):
        self.currentScore+=1


def input_handling(context, playerObj=None):
    if context == "NameAssignmentContext":
        bNameAssigned = False
        while bNameAssigned == False:
            try:
                playerNameString = str(input(f"Enter a name for player {len(player.PlayerNames)}: "))
                for playerName in player.PlayerNames:
                    if playerNameString == playerName:
                        raise name_taken()
                return playerNameString
            except name_taken:
                print ("Name already taken. Try again\n")
    elif context == "ShootingContext":
        bShotMade = False
        while bShotMade == False:
            try:
                player_input = input(f"\nshot nr {6 - playerObj.remainingRounds} at: ")
                if TypeMatchingDict[player_input] not in playerObj.targetsDict:
                    raise wrong_input()
                return player_input
            except wrong_input:
                print("\nIncorrect input value, try again")
            except TypeError:
                print("\nIncorrect input value, try again")
            except KeyError:
                print("\nIncorrect input value, try again")   
    return "Unknown"


def initialize_game():
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              Biathlon

         a hit or miss game
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")


def begin_play(player0, player1):
    bIsGameOver = False
    while bIsGameOver == False:
        if player0.remainingRounds == 0 and player1.remainingRounds == 0:
            bIsGameOver = True
        elif player0.playerState == player_state.EPS_HasSpoon:
            print(f"\n{player0.playerName}, you got {player0.remainingRounds} shots\n")
            player0.load_TargetDict()
            player0.shoot(input_handling("ShootingContext", player0))
            player0.take_spoon()
            player1.give_spoon()
        elif player1.playerState == player_state.EPS_HasSpoon:
            print(f"\n{player1.playerName}, you got {player1.remainingRounds} shots\n")
            player1.load_TargetDict()
            player1.shoot(input_handling("ShootingContext", player1))
            player1.take_spoon()
            player0.give_spoon()
    return


def main():
    player0 = player(input_handling("NameAssignmentContext"))
    player1 = player(input_handling("NameAssignmentContext"))
    player0.playerState = player_state.EPS_HasSpoon
    initialize_game()
    begin_play(player0, player1)
    print(f"{player0.playerName}, you hit {player0.scoreBoard.currentScore} targets!")
    player0.load_TargetDict()
    print(f"{player1.playerName}, you hit {player1.scoreBoard.currentScore} targets!")
    player1.load_TargetDict()
    
    
main()