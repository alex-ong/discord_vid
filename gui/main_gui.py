"""
main gui for the program
"""

import time
import os
import tkinter as tk
from tkinter.messagebox import askyesno
from tkinterdnd2 import TkinterDnD, DND_FILES
from install.install_context import get_install_path
from gui.task_status import TaskStatus

MAIN_APP = None
MAIN_GUI = None

ICON_PATH = "data/discordvidlogo-32.ico"

def exit_immediately():
    """exits the program immediately"""
    os._exit(0)  # pylint: disable-msg=protected-access


class MainApp(tk.Frame):
    """main frame for the program"""

    def __init__(self, root, task_queue):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("DiscordVid")
        self.root.protocol("WM_DELETE_WINDOW", self.on_gui_stop)
        self.root.iconbitmap(get_install_path() + "/" + ICON_PATH)

        self.is_closing = False
        self.last_preset = None
        # add task queue and spin off checking it every so often
        self.task_queue = task_queue  # tasks that need to be executed
        self.task_frame = tk.Frame(self)
        self.task_frame.grid()

        # register dropping files
        self.register_dropping()
        # start checking the queue
        self.check_queue()

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
        self.task_queue.manual_add_task(self.last_preset, path)

    def add_task(self, task):
        """Links a data-based task to the gui"""
        if self.is_closing:
            return

        task_gui = TaskStatus(self.task_frame)
        task_gui.grid()
        task_gui.set_task(task)
        self.last_preset = task.preset

    def on_gui_stop(self):
        """callback for when the gui stops"""
        if self.is_closing:
            return

        tasks_remaining = self.task_queue.get_remaining_tasks()
        if len(tasks_remaining) == 0:
            exit_immediately()

        if not show_quit_dialog():
            return  # they pressed "No", so don't quit

        # quitting "nicely"
        self.is_closing = True
        self.task_queue.cancel_all()
        time.sleep(1.0)
        exit_immediately()

    def check_queue(self):
        """Checks the task queue"""
        if self.root is None or self.is_closing:
            return
        task = self.task_queue.update()
        if task is not None:
            self.add_task(task)
        self.root.after(50, self.check_queue)


def show_quit_dialog():
    """shows the quit dialog"""
    answer = askyesno(
        title="Quit Confirmation", message="Are you sure that you want to quit?"
    )
    return answer


def main(task_queue):
    """main entrypoint to the program"""
    master = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()
    app = MainApp(master, task_queue)
    app.pack()
    master.mainloop()
