"""
Helper functions for registry adding and downloading files
"""
import sys
import ctypes  # Allows interface with low-level C API's
import os
import winreg  # Allows access to the windows registry
import requests


# ctypes constants and function pointer
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x1A
SMTO_ABORTIFHUNG = 0x0002
SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW


def add_to_path(program_path: str):
    """Takes in a path to a program and adds it to the system path"""
    if os.name == "nt":  # Windows systems
        with winreg.ConnectRegistry(
            None, winreg.HKEY_CURRENT_USER
        ) as root:  # Get the current user registry
            with winreg.OpenKey(
                root, "Environment", 0, winreg.KEY_ALL_ACCESS
            ) as key:  # Go to the environment key
                existing_path_value = winreg.EnumValue(key, 3)[
                    1
                ]  # Grab the current path value
                if existing_path_value[-1] != ";":
                    existing_path_value += ";"
                new_path_value = (
                    existing_path_value + program_path + ";"
                )  # Takes the current path value and appends the new program path
                winreg.SetValueEx(
                    key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value
                )  # Updated the path with the updated path

            # Tell other processes to update their environment
            result = ctypes.c_long()

            SendMessageTimeoutW(
                HWND_BROADCAST,
                WM_SETTINGCHANGE,
                0,
                "Environment",
                SMTO_ABORTIFHUNG,
                5000,
                ctypes.byref(result),
            )
    else:  # If system is *nix
        with open(
            f"{os.getenv('HOME')}/.bashrc", "a", encoding="utf8"
        ) as bash_file:  # Open bashrc file
            bash_file.write(
                f'\nexport PATH="{program_path}:$PATH"\n'
            )  # Add program path to Path variable
        os.system(f". {os.getenv('HOME')}/.bashrc")  # Update bash source
    print(
        f"Added {program_path} to path, please restart shell for changes to take effect"
    )


def download_file(source: str, dest: str):
    """
    Downloads a file from URL to destination, with a progress update
    """
    print(f"Downloading file from {source} to {dest}")
    with open(dest, "wb") as file:
        response = requests.get(source, stream=True, timeout=1.0)
        total_length = response.headers.get("content-length")

        if total_length is None:  # no content length header
            file.write(response.content)
        else:
            downloaded = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                file.write(data)
                done = int(50 * downloaded / total_length)
                done, not_done = "=" * done, " " * (50 - done)
                sys.stdout.write(f"\r[{done}{not_done}]")
                sys.stdout.flush()
