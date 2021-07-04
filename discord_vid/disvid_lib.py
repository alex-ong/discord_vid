"""
A bunch of useful library functions
"""
import sys
import subprocess

def check_nvidia():
    print("hi")
    args = "wmic path win32_VideoController get name"
    result = subprocess.run(args.split(), capture_output=True)    
    items = result.stdout.lower().split()
    items = [item.decode("utf-8") for item in items]

    if "nvidia" in items:
        return True
        
    return False

if __name__ == "__main__":        
    print(sys.argv)
    if "--check_nvidia" in sys.argv:        
        result = check_nvidia()
        print ("We have NVIDIA!")        
        sys.exit(0 if result else 1)
        
       
    sys.exit(0)