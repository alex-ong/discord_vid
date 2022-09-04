"""
Task status frame
"""

import tkinter as tk
from gui.labeledprogress import LabeledProgressBar
from discord_vid.task import Task


# style = ttk.Style()
# style.theme_use('clam')
# style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

PROGRESS_LENGTH = 280


def create_progressbar(root):
    """creates a labeled progress bar"""
    return LabeledProgressBar(root, length=PROGRESS_LENGTH, maximum=100)


class TaskStatus(tk.Frame):
    """Main frame for a single task"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.title = tk.Label(self, text="file name")
        self.title.grid(row=0, sticky=tk.W)
        self.expand_button = tk.Button(self, command=self.toggle_info)
        self.expanded = False

        self.history_frame = tk.Frame(self)
        self.history_frame.grid()

        self.progress_bar = create_progressbar(self.history_frame)
        self.progress_bar.grid()

        self.bars = [self.progress_bar]

        self.task = None
        self.rendering_task = None
        self.rendering_stopper = None

    def toggle_info(self):
        """toggles the info panels"""
        self.expanded = not self.expanded
        self.refresh_infos()

    def refresh_infos(self):
        """shows progress bars as appropriate"""
        for pbar in self.bars:
            pbar.grid_forget()

        if self.expanded:
            for pbar in self.bars:
                pbar.grid()
            self.expand_button.config(text="Less info...")
        else:
            self.bars[-1].grid()
            self.expand_button.config(text="More info...")

    def set_task(self, task: Task):
        """Sets the active task for this gui element"""
        self.task = task
        self.title["text"] = task.filename
        task.set_callbacks(self.on_task_start, self.on_task_update, self.on_task_finish)

    def on_task_start(self, task_info):
        """Callback for when the task starts"""
        print(task_info)

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
            self.progress_bar.set_color("red")
            self.progress_bar = create_progressbar(self.history_frame)
            self.bars.append(self.progress_bar)
            if len(self.bars) == 2:
                self.expand_button.grid(row=0, sticky=tk.E)
            self.refresh_infos()
        else:
            self.progress_bar.set_color("green")

    def on_task_stop(self, _):
        """triggered when the user cancels the task"""
        self.task.cancel()  # should end up calling task_update(error)
