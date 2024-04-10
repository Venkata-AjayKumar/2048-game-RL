""" For creating a new window, see root.py
    Construct a Main View (see window.py)
"""
from gui.root import new_root
from gui.window import Window


def start():
    root = new_root()
    Window(root)  # create a main window

    # start the main window
    root.mainloop()  # blocking function (i.e. function never returns)
