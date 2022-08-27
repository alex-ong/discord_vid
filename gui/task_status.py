"""
Task status frame
"""

import tkinter as tk
from gui.labeledprogress import LabeledProgressBar
from gui.task_args import TaskArgs
from discord_vid.task import Task


# style = ttk.Style()
# style.theme_use('clam')
# style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

PROGRESS_LENGTH = 280


class TaskStatus(tk.Frame):
    """Main frame for a single task"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.title = tk.Label(self, text="file name")
        self.title.grid()

        self.progress_bar = self.create_progressbar()
        self.progress_bar.grid()

        self.task_args = TaskArgs(self)
        self.task_args.grid()

        self.is_open = False  # expanded or not
        self.expand_button = None  # todo
        self.task_root = None  # todo
        self.task = None  # todo

    def create_progressbar(self):
        """creates a new progressbar"""
        return LabeledProgressBar(self, length=PROGRESS_LENGTH, maximum=100)

    def set_task(self, task: Task):
        """Sets the active task for this gui element"""
        self.task = task
        self.title["text"] = task.filename
        self.task_args.set_task(task)
        task.set_on_update(self.on_task_update)
        task.set_on_finish(self.on_task_finish)

    def on_task_update(self, seconds_processed, subtask_count):
        """Callback for when the task updates"""
        current_task, num_subtasks = subtask_count
        perc = seconds_processed / self.task.video_length * 100 / num_subtasks
        self.progress_bar["value"] = (current_task * 100.0 / num_subtasks) + perc
        self.progress_bar.auto_set_label_perc()

    def on_task_finish(self, finished, message):
        """updates progressbar color when the task is finished"""
        self.progress_bar["value"] = self.progress_bar["maximum"]
        self.progress_bar.set_label(message)
        if not finished:
            self.progress_bar = self.create_progressbar()
            self.progress_bar.grid()

    def on_task_stop(self, _):
        """triggered when the user cancels the task"""
        self.task.cancel()  # should end up calling task_update(error)
