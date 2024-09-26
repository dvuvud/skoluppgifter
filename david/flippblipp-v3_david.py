def flippblipp(n):
    if n % 3 == 0 and n % 5 == 0:
        return ("flipp blipp")
    elif n % 3 == 0:
        return ("flipp")
    elif n % 5 == 0:
        return("blipp")
    else:
        return(str(n))
            
def game():
    round = 1
    print(str(round))
    while(True):
        round += 1
        playerInput = input("Nästa: ")
        if playerInput == flippblipp(round):
            continue
        else:
            print("Fel - " + flippblipp(round))
            break
game()