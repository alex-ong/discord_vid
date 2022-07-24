"""
Main entrypoint to program.
Use program with preset and file.
"""
import sys
from discord_vid import disvid


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python -m discord_vid.disvid {PRESET} file.mp4")
        sys.exit()
    disvid.convert(sys.argv[1], sys.argv[2])
