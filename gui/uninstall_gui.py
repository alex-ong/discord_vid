"""
simple dialog box to uninstall
"""
import os
import tkinter as tk
from tkinter import messagebox
from install.install_context import uninstall_context

MSG = "Please press Yes a few times for Regedit to uninstall the discord_vid"
TITLE = "Uninstall discord_vid"


def show_warning(title, message, func, exit_program=True):
    """
    Shows messagebox warning
    """
    messagebox.showinfo(
        title,
        message,
    )
    try:
        func()
    except OSError:  # user hit cancel
        pass
    if exit_program:
        os._exit(0)  # pylint: disable-msg=protected-access


def main(title=TITLE, msg=MSG, func=uninstall_context):
    """runs the installer gui app"""
    master = tk.Tk()
    master.title(title)
    master.iconify()
    master.after(1, lambda: show_warning(title, msg, func))
    master.mainloop()
