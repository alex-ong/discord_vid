"""
Main entrypoint to program.
Use program with preset and file.
"""
import sys
import os

from discord_vid.preset import display_presets
from discord_vid.task import Task
from discord_vid.taskqueue import TaskQueue
from gui.main_gui import main as gui_main
from gui.install_gui import main as install_main
from gui.uninstall_gui import main as uninstall_main
from gui.noargs import get_error_msg, show_noargs

USE_GUI = True


def convert_no_gui(preset, path):
    """converts a task without the gui"""
    task = Task(preset, path)
    task.generate_file()


def main_non_convert():
    """
    handles installing and uninstalling context hooks
    returns if we should exit the program
    """
    if "--install" in sys.argv:
        install_main()
    elif "--uninstall" in sys.argv:
        uninstall_main()
    elif len(sys.argv) < 3:
        msg = get_error_msg(*display_presets())
        if USE_GUI:
            show_noargs(msg)
        else:
            print(msg)
            print(sys.argv[0] + " PRESET file.mp4")
            input("Press enter to continue...")
    else:
        return False
    return True


def main_convert(preset, path):
    """main function for processing argv and then running program"""
    task_queue = TaskQueue()
    task_queue.send_task(preset, path)
    if task_queue.is_master_queue():
        gui_main(task_queue)  # start the gui
    else:
        os._exit(0)  # pylint: disable-msg=protected-access


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
    if main_non_convert():  # handle args first
        sys.exit()
    if USE_GUI:
        main_convert(sys.argv[1], sys.argv[2])
    else:
        convert_no_gui(sys.argv[1], sys.argv[2])
