"""
Main entrypoint for command line based conversion
"""

from discord_vid.task import Task


def convert(task: Task):
    """
    Converts a given filename using the provided preset
    """
    task.generate_file()
