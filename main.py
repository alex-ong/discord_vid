"""
Main entrypoint to program.
Use program with preset and file.
"""
import sys
import os

from install import install_context
from discord_vid.task import Task
from discord_vid.preset import display_presets
from discord_vid.zmq_service import ZMQService
from gui.main_gui import main as gui_main, get_gui, get_app
from gui.install_gui import main as install_main
from gui.uninstall_gui import main as uninstall_main

USE_GUI = True


def halt_on_exception(exception_type, value, traceback, oldhook=sys.excepthook):
    """Whenever there is a exception, require user to press enter"""
    oldhook(exception_type, value, traceback)
    print("=" * 20)
    input("Please copy the error and report to the developer")


# sys.excepthook = halt_on_exception


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
    elif len(sys.argv) < 3 and not USE_GUI:
        print(sys.argv[0] + " PRESET file.mp4")
        display_presets()
        print("sample:")
        print(sys.argv[0] + " default file.mp4")
        input("Press enter to continue...")
    else:
        return False
    return True

def main_convert(preset, path):
    """main function for processing argv and then running program"""
    service = ZMQService()
    if service.server is not None:
        gui_main()  # start the gui
        app = get_app()
        app.add_task_queue(service)
        service.client.send(preset, path)
        get_gui().mainloop()
    else:
        service.client.send(preset, path)
        os._exit(0)  # pylint: disable-msg=protected-access


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
    if main_non_convert():  # handle args first
        sys.exit()
    if USE_GUI:
        main_convert(sys.argv[1], sys.argv[2])
    else:
        convert_no_gui(sys.argv[1], sys.argv[2])
