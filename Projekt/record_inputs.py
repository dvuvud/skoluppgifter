import ctypes # to check the current keystate
import msvcrt # to take inputs

pressed_keys = []
bEnterLastFrame = False
KEY_ENTER = 0x0D
KEY_SHIFT = 0x10

def is_key_pressed(key):
    state = ctypes.windll.user32.GetAsyncKeyState(key)
    return state & 0x8000 != 0 # if the state of the key is the highest possible bit (state = 0x8000), the key is being pressed 


def on_press():
    global bEnterLastFrame
    while True:

        """
        "" msvcrt.getch() waits for input so if enter is held down while typing, and released after typing,
        "" The function wont return when enter is pressed until another key is entered
        """
        if is_key_pressed(KEY_ENTER):
            if not bEnterLastFrame:
                bEnterLastFrame = True
                if len(pressed_keys) > 0: # returns if there is any text (can't send empty messages)
                    return
        else:
            bEnterLastFrame = False


        keypress = msvcrt.getch() # returns a single keypress
        key = keypress.decode('utf-8')

        if is_key_pressed(KEY_ENTER): # stops typing if key is held down, temporary fix to problem
            continue

        if key == '\x08': # checks for backspace
            if len(pressed_keys) > 0:
                del pressed_keys[-1]
                print('\b', end='')
                print(' ', end='')
                print('\b', end='')
            continue
        elif key == ' ': # checks for space
            print(' ', end='')
            pressed_keys.append(' ')
            continue
        elif key.isalpha():
            if is_key_pressed(KEY_SHIFT):
                pressed_keys.append((key).upper())
                print(pressed_keys[-1], end='')
                continue
            pressed_keys.append(key)
            print(pressed_keys[-1], end='')
            continue
        elif key.isdigit():
            pressed_keys.append(key)
            print(pressed_keys[-1], end='')
            continue
        elif key in {'.', ',', '-', '_', '?'}:
            pressed_keys.append(key)
            print(pressed_keys[-1], end='')
            continue


def take_input():
    on_press()
    chat_message = ''.join(pressed_keys)
    pressed_keys.clear()
    return chat_message