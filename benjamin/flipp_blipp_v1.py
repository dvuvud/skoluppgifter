n = 50

for number in range(n):
    number = number + 1

    if number % 3 == 0 and number % 5 == 0:
        print("flipp blipp")

    elif number % 3 == 0:
        print("flipp")

    elif number % 5 == 0:
        print("blipp")
    
    else:
        print(number)