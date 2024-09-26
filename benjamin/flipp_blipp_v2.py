def flipp_blipp(number):
    if number % 3 == 0 and number % 5 == 0:
        to_say = "flipp blipp"

    elif number % 3 == 0:
        to_say = "flipp"

    elif number % 5 == 0:
        to_say = "blipp"

    else:
        to_say = number

    return to_say

n = 50

for number in range(n):
    print(flipp_blipp(number + 1))