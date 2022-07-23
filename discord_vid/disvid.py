from discord_vid import disvid_lib
from discord_vid import disvid_libx264
from discord_vid import disvid_nvenc
from discord_vid.preset import Preset
import sys





def convert(preset: str, filename):
    preset = Preset.from_str(preset)
    print(f"Converting {filename} using {preset.name}")
    has_nvidia = disvid_lib.check_nvidia()
    # choose encoder
    # do encoder in loop


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python -m discord_vid.disvid {PRESET} file.mp4")
        sys.exit()
    convert(sys.argv[1], sys.argv[2])