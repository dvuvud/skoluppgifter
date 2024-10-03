import random

def generate_target_visualization(targets):
    target_states_visual = []

    for target in targets:
        target_state = target[1]

        if(target_state == 0):
            target_states_visual.append("O")
        else:
            target_states_visual.append("[]")
        
    return " ".join(target_states_visual)

def shoot_at_target(targets, target_number):
    # uppdatera andra indexet i target till 1, vilket innebär stängd/träffad
    target = targets[target_number - 1]

    if(target[1] == 1):
        print("Miss!")
        return targets
    
    hit_percentage = 80
    roll = random.randint(1,100)

    if(roll < hit_percentage):
        targets[target_number - 1][1] = 1
        print("Hit on target " + str(target_number) + "!")
    else:
        print("Miss!")

    return targets

def get_target_number_input():
    valid_input = False

    while valid_input == False:
        try:
            user_input = input("Shoot at: ")
            
            user_input_converted = int(user_input)

            if(user_input_converted > 0 and user_input_converted < 6):
                valid_input = True
        except:
            print("Invalid input")

    return user_input_converted

def get_score(targets):
    score = 0

    for target in targets:
        if(target[1] == 1):
            score += 1

    return score

targets = [
    [1,0],
    [2,0],
    [3,0],
    [4,0],
    [5,0]
]

for _ in range(5):
    print(generate_target_visualization(targets))

    user_input = get_target_number_input()

    shoot_at_target(targets, user_input)

print("------------------")
print("You hit " + str(get_score(targets)) + " out of 5 targets.")