"""
Task queueing class
For when we have way too many tasks
"""
from discord_vid.config import get_config


class TaskQueue:
    """Task Queueing class"""

    def __init__(self):
        self.tasks = []
        self.concurrency = get_config()["simultaneous_tasks"]

    def add_task(self, task):
        """Add task to queue"""
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove task from queue"""
        self.tasks.remove(task)

    def update(self):
        """updates the task queue"""
        return
