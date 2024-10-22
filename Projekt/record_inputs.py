
import ctypes # to check the current keystate
import msvcrt # to take inputs

pressed_keys = []
KEY_SHIFT = 0x10

def is_key_pressed(key):
    state = ctypes.windll.user32.GetAsyncKeyState(key)
    return state & 0x8000 != 0 # if the state of the key is the highest possible bit (state = 0x8000), the key is being pressed 


def on_press():
    while True:
        keypress = msvcrt.getch() # returns a single keypress
        key = keypress.decode('utf-8')
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
            if key == '\x00' or key == '\xe0': # checks if the key is shift
                continue
            if is_key_pressed(KEY_SHIFT):
                pressed_keys.append((key).upper())
                print(pressed_keys[-1], end='')
                continue
            pressed_keys.append(key)
            print(pressed_keys[-1], end='')
            continue
        elif key == '\r': # checks if the key is enter - > which returns the list
            return


def take_input():
    on_press()
    chat_message = ''.join(pressed_keys)
    pressed_keys.clear()
    return chat_message