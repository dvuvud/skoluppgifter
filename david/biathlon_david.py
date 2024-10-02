import random
from enum import Enum

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
    PlayerNames = []
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
    def give_spoon(self):
        self.playerState = player_state.EPS_HasSpoon
    def take_spoon(self):
        self.playerState = player_state.EPS_NotHasSpoon
        self.remainingRounds-=1
    def load_TargetDict(self):
        print(" ".join(self.targetsDict.keys()))
        print(" ".join(self.targetsDict.values()))
    def shoot(self, player_input, scoreBoard):
        hit_or_miss = random.choice(["◯", "⭐"])
        if hit_or_miss == "◯":
            print("\nMiss")
            return
        elif self.targetsDict[TypeMatchingDict[player_input]] == "◯":
            print("\nHit on open target")
            scoreBoard.add_to_score()
            self.targetsDict[TypeMatchingDict[player_input]] = hit_or_miss
            return
        elif self.targetsDict[TypeMatchingDict[player_input]] == "⭐":
            print("\nHit on closed target")
            return hit_or_miss  
    def __str__(self):
        return f"{self.playerName} is currently in state: {self.playerState.name}"
    
    
class score_board():
    def __init__(self, playerName):
        self.playerName = playerName
        self.currentScore = 0
    def add_to_score(self):
        self.currentScore+=1
    def get_score(self):
        return f"{self.playerName} has hit {self.currentScore} targets"


def input_handling(context, playerObj=None):
    if context == "NameAssignmentContext":
        bNameAssigned = False
        while bNameAssigned == False:
            try:
                playerNameString = str(input(f"Enter a name for player {len(player.PlayerNames)}: "))
                for playerName in player.PlayerNames:
                    if playerNameString == playerName:
                        raise name_taken()
            except name_taken:
                print ("Name already taken. Try again\n")
            else:
                return playerNameString
    elif context == "ShootingContext":
        bShotMade = False
        while bShotMade == False:
            try:
                player_input = input(f"\nshot nr {6 - playerObj.remainingRounds} at: ")
                if TypeMatchingDict[player_input] not in playerObj.targetsDict:
                    raise wrong_input()
            except wrong_input:
                print("\nIncorrect input value, try again")
            except TypeError:
                print("\nIncorrect input value, try again")
            except KeyError:
                print("\nIncorrect input value, try again")
            else:
                return player_input
    else:
        return "Unknown"


def initialize_game():
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              Biathlon

         a hit or miss game
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")


def begin_play(player0, player1, scoreBoard0, scoreBoard1):
    bIsGameOver = False
    currentRound = 0
    while bIsGameOver == False:
        currentRound+=1
        if player0.remainingRounds == 0 and player1.remainingRounds == 0:
            bIsGameOver = True
        elif player0.playerState == player_state.EPS_HasSpoon:
            print(f"\n{player0.playerName}, you got {player0.remainingRounds} shots\n")
            player0.load_TargetDict()
            player0.shoot(input_handling("ShootingContext", player0), scoreBoard0)
            player0.take_spoon()
            player1.give_spoon()
        elif player1.playerState == player_state.EPS_HasSpoon:
            print(f"\n{player1.playerName}, you got {player1.remainingRounds} shots\n")
            player1.load_TargetDict()
            player1.shoot(input_handling("ShootingContext", player1), scoreBoard1)
            player1.take_spoon()
            player0.give_spoon()
    return


def main():
    player0 = player(input_handling("NameAssignmentContext"))
    player1 = player(input_handling("NameAssignmentContext"))
    scoreBoard0 = score_board(player0.playerName)
    scoreBoard1 = score_board(player1.playerName)
    player0.playerState = player_state.EPS_HasSpoon
    initialize_game()
    begin_play(player0, player1, scoreBoard0, scoreBoard1)
    print(f"{player0.playerName}, you hit {scoreBoard0.currentScore} targets!")
    player0.load_TargetDict()
    print(f"{player1.playerName}, you hit {scoreBoard1.currentScore} targets!")
    player1.load_TargetDict()
    
    
main()