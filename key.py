from pynput import keyboard, mouse
from logger import log
from threading import Thread


def on_press(key):
    try:
        log(key.vk)
    except AttributeError:
        if key.name != 'space':
            log(int(str(key.value)[1:-1]))
        else:
            log(32)
    except:
        pass


def on_release(key):
    try:
        log(-key.vk)
    except AttributeError:
        if key.name != 'space':
            log(-int(str(key.value)[1:-1]) - 3)
        else:
            log(-32 - 3)
    except:
        pass


def on_click(x, y, button, pressed):
    try:
        log(-1, (int(button.name == 'left') * 2 - 1) * x, (int(pressed) * 2 - 1) * y)
    except:
        pass


def on_scroll(x, y, dx, dy):
    try:
        log(-2, x, y, dx, dy)
    except:
        pass


class KeyThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as keylistener:
            keylistener.join()


class MouseThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        with mouse.Listener(
                on_click=on_click,
                on_scroll=on_scroll) as mouselistener:
            mouselistener.join()


if __name__ == '__main__':
    kthread = KeyThread()
    kthread.start()
    mthread = MouseThread()
    mthread.start()
