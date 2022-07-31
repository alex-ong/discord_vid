import os
import sys
INSTALL_SAMPLE = "data/sample_install.reg.bak"
INSTALL_ACTUAL = "data/install.reg"

def get_install_path():
    result = os.path.dirname(sys.argv[0])
    result = os.path.abspath(result)
    result = result.replace("\\","/")
    result = result.replace("/", "\\\\")
    return result

def get_install_exe():
    return get_install_path() + "\\\\dv.exe"

def get_install_ico():
    return get_install_path() + "/data/discordvidlogo-24-black.ico"

def generate_context():
    lines = []
    exe = get_install_exe()
    icon = get_install_ico()
    with open(INSTALL_SAMPLE, 'r') as file:
        for line in file:
            line = line.replace("{exe_path}", exe)
            line = line.replace("{icon_path}", icon)
            lines.append(line)

    for line in lines:
        print (line.strip())

    with open(INSTALL_ACTUAL, 'w') as file:
        file.writelines(lines)


    
# python -m install.install_context"
if __name__ == "__main__":
    generate_context()
