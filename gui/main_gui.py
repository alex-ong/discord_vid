"""
main gui for the program
"""

import time
import os
import tkinter as tk
from tkinter.messagebox import askyesno
from tkinterdnd2 import TkinterDnD, DND_FILES

from gui.task_status import TaskStatus
from discord_vid.task import Task

MAIN_APP = None
MAIN_GUI = None


class MainApp(tk.Frame):
    """main frame for the program"""

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("DiscordVid")
        self.root.protocol("WM_DELETE_WINDOW", self.on_gui_stop)
        self.is_closing = False
        self.tasks = []
        self.task_queue = None

        self.task_frame = tk.Frame(self)
        self.task_frame.grid()

        # register dropping
        self.register_dropping()
        self.last_preset = None

    def register_dropping(self):
        """register this applicaiton for drag/dropping files"""
        self.drop_target_register(DND_FILES)  # pylint: disable=no-member
        self.dnd_bind(  # pylint: disable=no-member
            "<<Drop>>", lambda e: self.on_drop_file(e.data)
        )
        drop_label = tk.Label(
            self, text="Drag more video files here", borderwidth=3, relief="groove"
        )
        drop_label.grid()

    def on_drop_file(self, path):
        """callback for when user drops file"""
        task = Task(self.last_preset, path)
        self.add_and_run_task(task)

    def add_task(self, task):
        """Adds a task to the gui"""
        if self.is_closing:
            return

        self.tasks.append(task)
        task_gui = TaskStatus(self.task_frame)
        task_gui.grid()
        task_gui.set_task(task)
        self.last_preset = task.preset

    def add_and_run_task(self, task):
        """add a task and run it immediately"""
        if self.is_closing:
            return
        self.add_task(task)
        task.generate_file()

    def on_gui_stop(self):
        """callback for when the gui stops"""
        if self.is_closing:
            return
        tasks_remaining = [task for task in self.tasks if not task.finished]
        if len(tasks_remaining) > 0:
            confirm_quit = show_quit_dialog()
        else:
            os._exit(0)  # pylint: disable-msg=protected-access

        if not confirm_quit:
            return

        self.is_closing = True
        for task in self.tasks:
            task.cancel()

        time.sleep(1.0)
        os._exit(0)  # pylint: disable-msg=protected-access

    def add_task_queue(self, queue):
        """adds a zmq_service that can be checked for new things to process"""
        if self.task_queue is not None:
            raise ValueError("You can only set this once!")
        self.task_queue = queue
        self.check_queue()

    def check_queue(self):
        """Checks the a task queue"""
        if self.root is None or self.is_closing:
            return
        task = self.task_queue.update()
        if task is not None:
            self.add_and_run_task(task)
        self.root.after(50, self.check_queue)


def show_quit_dialog():
    """shows the quit dialog"""
    answer = askyesno(
        title="Quit Confirmation", message="Are you sure that you want to quit?"
    )
    return answer


def main():
    """main entrypoint to the program"""
    global MAIN_APP  # pylint: disable-msg=global-statement
    global MAIN_GUI  # pylint: disable-msg=global-statement
    master = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()
    app = MainApp(master)
    app.pack()
    MAIN_GUI = master
    MAIN_APP = app


def get_gui():
    """Returns the tkinter root gui if it exists"""
    return MAIN_GUI


def get_app():
    """Returns the main frame for the entire application"""
    return MAIN_APP


if __name__ == "__main__":
    main()
