import random


class wrong_input(Exception):
    pass    
    
    
def shoot(shot,targets):
    list = ["*","0"]
    hit_or_nah = random.choice(list)
    if hit_or_nah == "*":
        print("\nMiss\n")
        return hit_or_nah
    elif targets[shot] == "*":
        print("\nHit on open target\n")
        return hit_or_nah        
    elif targets[shot] == "0":
        print("\nHit on closed target\n")
        return hit_or_nah   


def biathlon():
    list_of_nums = [1,2,3,4,5]
    target_dict = {
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
    for i in range(5):
        round_nr = i+1
        print(" ".join(str(num) for num in list_of_nums))
        print(" ".join(str(target_dict[key]) for key in ["1", "2", "3", "4", "5"]))
        while True:
            try:
                player_shot = input(f"shot nr {round_nr} at: ")
                if player_shot not in target_dict:
                    raise wrong_input()
            except wrong_input:
                print("\nIncorrect value, try again\n")
            else:
                target_dict[player_shot] = shoot(player_shot, target_dict)
                break
    print(" ".join(str(num) for num in list_of_nums))
    print(" ".join(str(target_dict[key]) for key in ["1", "2", "3", "4", "5"]))
    number_of_hits = list(target_dict.values()).count("0")
    print(f"\nYou hit {number_of_hits} of 5 targets")
    
biathlon()