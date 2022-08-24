"""
main gui for the program
"""

import tkinter as tk
from gui.task_status import TaskStatus

MAIN_APP = None


class MainApp(tk.Frame):
    """main frame for the program"""

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # self.task_pane = tk.Frame(self)
        tk.Label(self, text="hello world").grid()

    def add_task(self, task):
        """Adds a task to the gui"""
        task_gui = TaskStatus(self)
        task_gui.grid()
        task_gui.set_task(task)
        # self.task_pane.add_task(task)


def manual_update(root):
    """Manually update the gui every 16ms"""
    root.update()
    if root is not None:
        root.after(16, lambda: manual_update(root))


def main():
    """main entrypoint to the program"""
    global MAIN_APP  # pylint: disable-msg=global-statement
    master = tk.Tk()
    app = MainApp(master)
    app.pack()
    manual_update(master)
    MAIN_APP = app


def get_gui():
    """Returns the main gui if it exists"""
    return MAIN_APP


if __name__ == "__main__":
    main()
