import threading
import time
import keyboard


pressed_keys = []
input_question_thing = "Enter something:"
def random_messages():
    while True:
        message = "I love oranges"
        print('\r', end='') # flyttar kursorn längst till vänster på den rad den befinner sig på
        print("\033[K", end='') # tar bort allt som är till höger av cursorn
        print(message) # printa meddelandet på samma rad som man tog bort input_question_thing nyss (cursorn hamnar då automatiskt på nästa rad)
        print(input_question_thing, ''.join(pressed_keys), end='') # print input_question_thingy och stanna på samma rad samt printa de knappar man tryck på innan
        time.sleep(1) # bara för att testa funktionen av grejsen


def on_press(event):
    if event.name == 'enter': # här kan man lägga till något som skickar samlingen av alla pressed_keys till servern när man trycker enter
        pressed_keys.clear()
        print('\r', end='') # flyttar kursorn längst till vänster på den rad den befinner sig på
        print("\033[K", end='') # tar bort allt som är till höger av cursorn
        print(input_question_thing, end='')
        return
    elif event.name == 'backspace': # tar bort den sista bokstaven om det är backspace 
        if len(pressed_keys) > 0:
            del pressed_keys[-1]
            print('\b', end='')
            print(' ', end='')
            print('\b', end='')
        return
    elif event.name == 'space': # lägger till ett mellanrum om det är "space"
        print(' ', end='')
        pressed_keys.append(' ')
        return
    elif event.name.isalpha():  # kollar om det är en bokstav i alfabetet
        if keyboard.is_pressed('skift'): # gör till uppercase
            if event.name != 'skift':
                pressed_keys.append((event.name).upper())
                print(pressed_keys[-1], end='')
                return
            elif event.name == 'skift':
                return
        pressed_keys.append(event.name)
        print(pressed_keys[-1], end='')
        return


def take_input():
    keyboard.on_press(on_press) # binder en delegat som tar en parameter (event) vilket håller informationen om knappen man tryckt på


def message_input_thing():
    input_thread = threading.Thread(target=random_messages)
    input_thread.daemon = True
    input_thread.start()
    take_input()
    keyboard.wait('esc')
    return


message_input_thing()