"""
Main entrypoint to program.
Use program with preset and file.
"""
import sys
from discord_vid import disvid
from install import install_context

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
        print("python -m discord_vid.disvid {PRESET} file.mp4")
        input("Press enter to continue...")
        sys.exit()
    disvid.convert(sys.argv[1], sys.argv[2])
