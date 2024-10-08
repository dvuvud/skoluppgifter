import random, time

def show_splash():
    print("\n======================================")
    print("    BIATHLON - A HIT OR MISS GAME    ")
    print("======================================\n")

def create_players(player_amount):
    players = []

    for x in range(player_amount):
        targets = [False] * 5
    
        players.append([x + 1, targets])

    return players


def generate_target_visualization(targets):
    target_visual = []

    for target in targets:
        if(target == False):
            target_visual.append("O")
        else:
            target_visual.append("[]")
        
    return " ".join(target_visual)

def shoot_at_target(targets, target_number):
    target = targets[target_number - 1]
    
    hit_percentage = 80
    roll = random.randint(1,100)

    if(roll < hit_percentage):
        if(target == True):
            print("\nHit on already closed target!")
            return targets

        targets[target_number - 1] = True
        print("\nHit on target " + str(target_number) + "!")
        print(generate_target_visualization(targets))
    else:
        print("\nMiss!")

    return targets

def get_number_input(min, max, message):
    valid_input = False

    while valid_input == False:
        try:
            user_input = input(message)
            
            user_input_converted = int(user_input)

            if(user_input_converted >= min and user_input_converted <= max):
                valid_input = True
        except:
            print("Invalid input")

    return user_input_converted

def show_winner(players):
    player_ids_with_highest_score = []
    highest_score = 0

    for player in players:
        targets = player[1]

        score = 0
        for target in targets:
            if(target == True):
                score += 1

        if score > highest_score:
            player_ids_with_highest_score = [player[0]]
            highest_score = score
        elif score == highest_score:
            player_ids_with_highest_score.append(player[0])

    if len(player_ids_with_highest_score) > 1:
        print("\nIt's a tie between players " + ", ".join(map(str, player_ids_with_highest_score)) + "!")
    else:
        print("\nPlayer " + str(player_ids_with_highest_score[0]) + " wins!")

        
def main():
    show_splash()

    amount_of_players = get_number_input(1, 10, "Choose amount of players (1-10): ")
    
    players = create_players(amount_of_players)

    for round in range(1,6):
        for player in players:
            print("\n==== ROUND " + str(round) + ", Player " + str(player[0]) + " ====\n")

            targets = player[1]

            print(generate_target_visualization(targets))
            
            target_to_shoot_at = get_number_input(1, 5, "\nSelect target to shoot at (1-5): ")
            targets = shoot_at_target(targets, target_to_shoot_at)

            time.sleep(2)

    show_winner(players)

main()