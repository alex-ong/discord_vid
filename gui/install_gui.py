"""
Installation gui
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from discord_vid.config import get_config, save_config
from install import install_context
import os

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
        self.default_frame.grid(row=1,sticky=tk.NSEW)

        self.install_button = tk.Button(
            self, text="Install selected presets", command=self.install
        )
        self.install_button.grid(row=2)

    def add_button_frame(self):
        """adds the checkbuttons"""
        self.checks.clear()
        check_frame = tk.Frame(self)
        tk.Label(check_frame, text="Select presets to install in context menu").grid()
        keys = list(self.config["presets"].keys())
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
        tk.Label(default_frame, text="Default Preset").grid(row=0,sticky=tk.W)

        self.default_preset = tk.StringVar(self)
        self.default_preset.set(self.get_valid_keys()[0])
        self.default_preset_om = tk.OptionMenu(
            default_frame, self.default_preset, *self.config["presets"].keys()
        )
        self.default_preset_om.grid(row=0,column=1,sticky=tk.E)
        default_frame.columnconfigure(0, weight=1)
        default_frame.columnconfigure(1, weight=1)
        return default_frame

    def install(self):
        """installs the presets"""
        existing_keys = list(self.config["presets"].keys())
        valid_keys = self.get_valid_keys()
        keys_to_delete = [key for key in existing_keys if key not in valid_keys]
        print(f"Delete: {keys_to_delete}")
        for key in keys_to_delete:
            del self.config["presets"][key]

        save_config(self.config)
        # calls regedit and does the installation
        show_warning(True)

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



def show_warning(exit_program=True):
    """
    Shows messagebox warning
    """
    messagebox.showinfo('Regedit instructions', 'Please press Yes a few times for Regedit to install discord_vid')
    try:
        install_context.generate_context()
        install_context.install_context()
    except OSError: # user hit cancel
        pass
    if exit_program:
        os._exit(0)  # pylint: disable-msg=protected-access

def main():
    """runs the installer gui app"""
    master = tk.Tk()
    app = InstallApp(master)
    app.grid()
    master.mainloop()
