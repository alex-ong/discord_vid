"""
Main entrypoint to program.
Use program with preset and file.
"""
import sys
from install import install_context
from discord_vid.task import Task
from discord_vid.preset import display_presets

from gui.main_gui import main as gui_main, get_gui, get_app


def halt_on_exception(exception_type, value, traceback, oldhook=sys.excepthook):
    """Whenever there is a exception, require user to press enter"""
    oldhook(exception_type, value, traceback)
    print("=" * 20)
    input("Please copy the error and report to the developer")


# sys.excepthook = halt_on_exception


def convert(preset, path):
    """
    converts a preset and path to a task then executes it
    """
    task = Task(preset, path)
    gui = get_gui()
    if gui is not None:
        app = get_app()
        app.add_and_run_task(task)
    else:
        task.generate_file()


def main_convert():
    """main function for processing argv and then running program"""
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

    convert(sys.argv[1], sys.argv[2])


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
    gui_main()  # uncomment to enable gui
    tk_gui = get_gui()
    if tk_gui is not None:
        tk_gui.after(1, main_convert)
        tk_gui.mainloop()
    else:
        main_convert()
