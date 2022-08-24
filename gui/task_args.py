"""
Task arguments; an array of input and output arguments
"""
import tkinter as tk
from discord_vid.task import Task


class TaskArgs(tk.Frame):
    """
    Simple class to show the arguments fed to ffmpeg
    """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.input_entry = tk.Entry(self, text="inputs")
        self.output_entry = tk.Entry(self, text="outputs")
        self.bitrates = tk.Entry(self, text="bitrates")

        self.input_entry.grid(row=0, column=0)
        self.output_entry.grid(row=0, column=1)
        self.bitrates.grid(row=0, column=2)
        self.task = None

    def set_task(self, task: Task):
        """Initialises the gui by injecting the data"""
        self.task = task
