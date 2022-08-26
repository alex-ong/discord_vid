"""
Task status frame
"""

import tkinter as tk
from tkinter import ttk
from gui.task_args import TaskArgs
from discord_vid.task import Task

PROGRESS_LENGTH = 280


class TaskStatus(tk.Frame):
    """Main frame for a single task"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.title = tk.Label(self, text="file name")
        self.title.grid()

        self.progress_bar = ttk.Progressbar(self, length=PROGRESS_LENGTH)
        self.progress_bar.grid()  # todo

        self.task_args = TaskArgs(self)
        self.task_args.grid()

        self.is_open = False  # expanded or not
        self.expand_button = None  # todo
        self.task_root = None  # todo
        self.task = None  # todo

    def set_task(self, task: Task):
        """Sets the active task for this gui element"""
        self.task = task
        self.title["text"] = task.filename
        self.task_args.set_task(task)

    def on_task_update(self, update):
        """Callback for when the task updates"""
        self.progress_bar.percent = update.percent

    def on_task_stop(self, _):
        """triggered when the user cancels the task"""
        self.task.cancel()  # should end up calling task_update(error)