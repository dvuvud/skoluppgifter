import random


class wrong_input(Exception):
    pass    
    
    
def shoot(player_input,targets):
    hit_or_miss = random.choice(["*", "O"])
    if hit_or_miss == "*":
        print("\nMiss\n")
        return hit_or_miss
    elif targets[player_input] == "*":
        print("\nHit on open target\n")
        return hit_or_miss        
    elif targets[player_input] == "O":
        print("\nHit on closed target\n")
        return hit_or_miss  

def filter_input(targets, currentRound):
    while True:
        try:
            player_input = input(f"shot nr {currentRound} at: ")
            if player_input not in targets:
                raise wrong_input()
        except wrong_input:
            print("\nIncorrect value, try again\n")
        else:
            return player_input


def beginPlay(targets):
    for i in range(5):
        currentRound = i+1
        print(" ".join(targets.keys()))
        print(" ".join(targets.values()))
        player_input = filter_input(targets, currentRound)
        targets[player_input] = shoot(player_input, targets)
    return targets

def biathlon():
    targets = {
        "1":"*",
        "2":"*",
        "3":"*",
        "4":"*",
        "5":"*"}
    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              Biathlon

         a hit or miss game
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
    print("\nYou got 5 shots\n")
    targets = beginPlay(targets)
    print(" ".join(targets.keys()))
    print(" ".join(targets.values()))
    number_of_hits = list(targets.values()).count("O")
    print(f"\nYou hit {number_of_hits} of 5 targets")
    
biathlon()