"""
Main entrypoint to program.
Use program with preset and file.
"""
import sys
from install import install_context
from discord_vid import disvid
from discord_vid.task import Task
from discord_vid.preset import display_presets

def convert(preset, path):
    """
    converts a preset and path to a task then executes it
    """
    task = Task(preset, path)
    disvid.convert(task)


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
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
