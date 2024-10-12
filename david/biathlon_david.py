import random
import time
from enum import Enum
from typing import List

TypeMatchingDict = {
    "1":"１",
    "2":"２",
    "3":"３",
    "4":"４",
    "5":"５"
    }

class game_instance():
    def __init__(self):
        self.playerInstances = []

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
            type_text(f"\n{self.playerName} missed the target\n")
            return
        elif self.targetsDict[TypeMatchingDict[player_input]] == "◯":
            type_text(f"\n{self.playerName} hit an open target\n\n")
            self.scoreBoard.add_to_score()
            self.targetsDict[TypeMatchingDict[player_input]] = hit_or_miss
            self.load_TargetDict()
            return
        elif self.targetsDict[TypeMatchingDict[player_input]] == "⭐":
            type_text("\n{self.playerName} hit a closed target\n")
            return
    
    
class score_board():
    def __init__(self):
        self.currentScore = 0
    def add_to_score(self):
        self.currentScore+=1

def type_text(text):
    for char in text:
        delay = random.uniform(0.05, 0.15)
        print(char, end='', flush=True)
        time.sleep(delay)

def IH_name_assignment_context():
    bNameAssigned = False
    while bNameAssigned == False:
        try:
            playerNameString = str(input(f"\nEnter a name for player {len(player.PlayerNames)}: "))
            for playerName in player.PlayerNames:
                if playerNameString == playerName:
                    raise name_taken()
            return playerNameString
        except name_taken:
            print ("\nName already taken. Try again")
    return 0
    

def IH_shooting_context(playerObj):
    bShotMade = False
    while bShotMade == False:
        try:
            player_input = input(f"\nshot nr {6 - playerObj.remainingRounds} at: ")
            if player_input not in TypeMatchingDict:
                raise wrong_input()
            return player_input
        except wrong_input:
            print("\nIncorrect input value, try again")
    return 0


def IH_init_player_context():
    bAmountChosen = False
    while bAmountChosen == False:
        try:
            player_input = int(input("\nEnter desired number of players (Min 1)(Max 10): "))
            if player_input < 1 or player_input > 10:
                raise wrong_input()
            return player_input
        except wrong_input:
            print("\nAmount outside scope, try again")
        except ValueError:
            print("\nExpecting int, try again")
    return 0


def input_handling(context, playerObj=None):
    if context == "NameAssignmentContext":
        return IH_name_assignment_context()
    elif context == "ShootingContext":
        return IH_shooting_context(playerObj)
    elif context == "InitPlayerContext":
        return IH_init_player_context()
    return "Unknown"


def init_player_instances(playerAmount, gameInstanceObject):
    for _ in range (playerAmount):
        new_player = player(input_handling("NameAssignmentContext"))
        gameInstanceObject.playerInstances.append(new_player)


def initialize_game():
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              Biathlon

         a hit or miss game
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")


def begin_play(gameInstanceObject):
    bIsGameOver = False
    while bIsGameOver == False:
        for playerObj in gameInstanceObject.playerInstances:
            if playerObj.remainingRounds > 0:
                playerObj.give_spoon()
            else:
                bIsGameOver = True
                continue
            if playerObj.playerState == player_state.EPS_HasSpoon:
                type_text(f"\n{playerObj.playerName}, you got {playerObj.remainingRounds} shot(s)\n\n")
                playerObj.load_TargetDict()
                playerObj.shoot(input_handling("ShootingContext", playerObj))
                playerObj.take_spoon()
                continue
    return


def main():
    gameInstance = game_instance()
    init_player_instances(input_handling("InitPlayerContext"), gameInstance)
    initialize_game()
    begin_play(gameInstance)
    for playerObj in gameInstance.playerInstances:
        type_text(f"\n{playerObj.playerName}, you hit {playerObj.scoreBoard.currentScore} targets!\n")
        playerObj.load_TargetDict()
    
main()