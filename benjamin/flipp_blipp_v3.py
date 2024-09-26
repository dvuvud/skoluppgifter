def flipp_blipp(input):
    if number % 3 == 0 and number % 5 == 0:
        to_say = "flipp blipp"

    elif number % 3 == 0:
        to_say = "flipp"

    elif number % 5 == 0:
        to_say = "blipp"

    else:
        to_say = str(number)

    return to_say

number = 1
game_over = False

print(number)

while game_over == False:
    number += 1

    user_input = input("Nästa: ")
    correct_answer = flipp_blipp(number)

    if(user_input != correct_answer):
        print("Fel - " + correct_answer)
        print("Game over!")

        game_over = True