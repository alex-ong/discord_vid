"""
A class to hold rendering information
so that you can cancel it etc
"""


class RenderingTask(object):
    """
    Class to hold ffmpeg subtask information so that you can cancel it
    """

    def __init__(self, task_data, stop_event, on_update):
        self.stop_event = stop_event

        self.commands = task_data[0]
        self.output_file = task_data[1]
        self.cleanup = task_data[2]
        self.on_update = on_update

    def cancel(self):
        """stops the task"""
        print("stop event set")
        self.stop_event.set()
