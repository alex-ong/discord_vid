"""
Task queueing class
For when we have way too many tasks
"""
from discord_vid.config import get_config
from discord_vid.zmq_service import ZMQService


class TaskQueue:
    """Task Queueing class"""

    def __init__(self):
        self.zmq_service = ZMQService()
        self.tasks = []
        self.processing_tasks = []
        self.finished_tasks = []
        self.concurrency = get_config()["simultaneous_tasks"]

    def get_remaining_tasks(self):
        """return all tasks that are not finished"""
        return self.tasks + self.processing_tasks

    def send_task(self, preset, filename):
        """sends a task to a remote zmq_service"""
        self.zmq_service.client.send(preset, filename)

    def is_master_queue(self):
        """returns if we are the master TaskQueue"""
        return self.zmq_service.server is not None

    def manual_add_task(self, preset, path):
        """Add task to queue"""
        self.zmq_service.manual_add_task(preset, path)

    def update(self):
        """updates the task queue"""
        # first, move tasks from the zmq_service
        # to our internal queue
        self.update_running_tasks()

        task = self.zmq_service.update()
        if task is not None:
            self.tasks.append(task)
            return task
        return None

    def update_running_tasks(self):
        """update running task status"""
        # next, check how many tasks are running
        # and then start anything that needs starting
        for task in self.processing_tasks:
            if task.finished:
                self.processing_tasks.remove(task)
                self.finished_tasks.append(task)

        while len(self.processing_tasks) < self.concurrency and len(self.tasks) > 0:
            task = self.tasks.pop(0)
            task.generate_file()
            self.processing_tasks.append(task)

    def cancel_all(self):
        """cancel all running tasks"""
        for task in self.processing_tasks:
            task.cancel()
