"""
Installation gui
"""

import tkinter as tk
from tkinter import ttk
from discord_vid.config import get_config, save_config
from install.install_context import generate_and_install
from install.install_ffmpeg import install_ffmpeg, ffmpeg_installed
from gui.uninstall_gui import show_warning

INSTALL_INSTRUCTIONS = (
    "Please press Yes a few times for Regedit to install discord_vid.\n"
    + "When it's all done, shift+right click a video to test!"
)
INSTALL_FFMPEG = (
    "A command prompt will open, and download ffmpeg. please wait for it to complete"
)


class InstallFfmpeg(tk.Toplevel):
    """progress bar frame for ffmpeg"""

    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title = "Download and install ffmpeg"
        self.frame = tk.Frame(self)
        self.frame.pack()

        self.progress_label = tk.Label(self.frame, text="Downloading ffmpeg")
        self.progress_label.grid()
        self.progress_bar = ttk.Progressbar(
            self.frame, orient="horizontal", mode="determinate", length=280, maximum=1.0
        )
        self.progress_bar.grid()
        self.grab_set_global()
        self.update()
        install_ffmpeg(self.update_callback, True)

    def update_callback(self, data):
        """Called when ffmpeg installer has progress"""
        if data is None:
            self.destroy()
            return
        if isinstance(data, str):
            self.progress_label.config(text=data)
            self.progress_label.update()
        elif isinstance(data, float):
            self.progress_bar["value"] = data
            self.progress_bar.update()
        self.update()


class InstallApp(tk.Frame):
    """main frame for the program"""

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("DiscordVid Installation")
        self.checks = []
        self.install_frame = InstallFrame(self)
        self.install_frame.grid()


class InstallFrame(tk.Frame):
    """simple frame for selecting which presets to install"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.config = get_config()
        self.checks = []
        self.default_preset = None
        self.default_preset_om = None

        self.check_frame = self.add_button_frame()
        self.check_frame.grid(row=0)

        self.default_frame = self.add_default_frame()
        self.default_frame.grid(row=1, sticky=tk.NSEW)

        self.install_button = tk.Button(
            self, text="Install selected presets", command=self.install
        )
        self.install_ffmpeg_check = self.add_ffmpeg_checkmark()

        self.install_ffmpeg_check.grid(row=2)
        self.install_button.grid(row=3)

    def add_ffmpeg_checkmark(self):
        """
        Creates a checkbutton for whether we want to install ffmpeg
        """
        result = ttk.Checkbutton(
            self,
            text="Install ffmpeg (required)",
        )

        if ffmpeg_installed():
            result.state(["!disabled", "!selected", "!alternate"])
        else:
            result.state(["disabled", "selected", "!alternate"])
        return result

    def add_button_frame(self):
        """adds the checkbuttons"""
        self.checks.clear()
        check_frame = tk.Frame(self)
        tk.Label(check_frame, text="Select presets to install in context menu").grid()
        keys = list(self.config.presets.keys())
        for name in keys:
            check_var = tk.BooleanVar(self)
            check_var.set(True)
            button = ttk.Checkbutton(
                check_frame, text=name, variable=check_var, command=self.update_default
            )
            button.grid(sticky=tk.W)
            self.checks.append((check_var, button))
        return check_frame

    def add_default_frame(self):
        """Adds frame to select default preset"""
        default_frame = tk.Frame(self)
        tk.Label(default_frame, text="Default Preset").grid(row=0, sticky=tk.W)

        self.default_preset = tk.StringVar(self)
        self.default_preset.set(self.get_valid_keys()[0])
        self.default_preset_om = tk.OptionMenu(
            default_frame, self.default_preset, *self.config.presets.keys()
        )
        self.default_preset_om.grid(row=0, column=1, sticky=tk.E)
        default_frame.columnconfigure(0, weight=1)
        default_frame.columnconfigure(1, weight=1)
        return default_frame

    def install(self):
        """installs the presets"""
        existing_keys = list(self.config.presets.keys())
        valid_keys = self.get_valid_keys()
        keys_to_delete = [key for key in existing_keys if key not in valid_keys]
        print(f"Delete: {keys_to_delete}")
        for key in keys_to_delete:
            del self.config.presets[key]

        save_config(self.config)

        if self.install_ffmpeg_check.instate(["selected"]):
            InstallFfmpeg()  # opens a TopLevel window
        self.install_registry()

    def install_registry(self):
        """Installs registry"""
        show_warning("Install", INSTALL_INSTRUCTIONS, generate_and_install)

    def update_default(self):
        """called whenever we change the default preset"""
        valid_keys = self.get_valid_keys()

        # update the options displayed:
        menu = self.default_preset_om.children["menu"]
        menu.delete(0, "end")
        for value in valid_keys:
            menu.add_command(
                label=value, command=lambda v=value: self.default_preset.set(v)
            )

        # Update the selection to something that exists
        if self.default_preset.get() not in valid_keys:
            if len(valid_keys) > 0:
                self.default_preset.set(valid_keys[0])

    def get_valid_keys(self):
        """return keys that are checked"""
        return [item[1]["text"] for item in self.checks if item[0].get()]


def main():
    """runs the installer gui app"""
    master = tk.Tk()
    app = InstallApp(master)
    app.grid()
    master.mainloop()
