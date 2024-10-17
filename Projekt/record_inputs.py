import threading
import time
import keyboard

pressed_keys = []


def on_press(event):
    if event.name == 'backspace': 
        if len(pressed_keys) > 0:
            del pressed_keys[-1]
            print('\b', end='')
            print(' ', end='')
            print('\b', end='')
        return
    elif event.name == 'space':
        print(' ', end='')
        pressed_keys.append(' ')
        return
    elif event.name.isalpha() and event.name != 'alt' and event.name != 'ctrl' and event.name != 'enter':
        if keyboard.is_pressed('skift'):
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
    keyboard.on_press(on_press)
    keyboard.wait('enter')
    keyboard.unhook_all()
    chat_message = ''.join(pressed_keys)
    pressed_keys.clear()
    return chat_message