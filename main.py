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
    """handles installing and uninstalling context hooks"""
    if "--install" in sys.argv:
        install_context.generate_context()
        print("Generated installer in data/install.reg")
        install_context.install_context()
        sys.exit()
    elif "--uninstall" in sys.argv:
        install_context.uninstall_context()
        sys.exit()

    if len(sys.argv) < 3:
        print(sys.argv[0] + " PRESET file.mp4")
        display_presets()
        print("sample:")
        print(sys.argv[0] + " default file.mp4")
        input("Press enter to continue...")
        sys.exit()


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
    main_non_convert()  # handle args first

    if USE_GUI:
        main_convert(sys.argv[1], sys.argv[2])
    else:
        convert_no_gui(sys.argv[1], sys.argv[2])
