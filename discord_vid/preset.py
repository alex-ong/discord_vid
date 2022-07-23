from enum import Enum
class Preset(Enum):
    EIGHT_MB_720P30 = 1
    EIGHT_MB_720P60 = 2
    FIFTY_MB_1080P30 = 3
    FIFTY_MB_1080P60 = 4
    DEFAULT = 5

    @staticmethod
    def from_str(label:str):
        result = Preset.from_intstr(label)
        if result is None:
            try:
                result = Preset[label.upper()]
            except KeyError:
                print(f"Invalid preset: {label}")
                return Preset.DEFAULT
        return result

    @staticmethod
    def from_intstr(label:str):
        try:
            value = int(label)
            return Preset(value)
        except:
            return None

