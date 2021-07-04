import sys
import subprocess
import glob
import os

TARGET_SIZE = 7600
FULL_SIZE_BYTES = 8*1024*1024
MIN_SIZE_BYTES = int(7.5*1024*1024)
AUDIO_RATE = 64
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
                             
    return float(result.stdout)

def get_index(strings, array):
    for string in strings:
        try:
            return sys.argv.index("-i")            
        except ValueError:
            pass
    return None
    
def delete_logs():
    file_list = glob.glob('ffmpeg2pass-*.log')
    # Iterate over the list of file_paths & remove each file.
    for file_path in file_list:    
        os.remove(file_path)
    
    file_list = glob.glob('ffmpeg2pass-*.mbtree')
    # Iterate over the list of file_paths & remove each file.
    for file_path in file_list:    
        os.remove(file_path)
    
def generate_file(target_size):
    bitrate = (target_size*8.0 - AUDIO_RATE*length)/ length
    if bitrate < 0:
        print(f"Unfortunately there is not enough bits for video!")
        sys.exit()
    
    
    command = (["ffmpeg", "-y"] + sys.argv[1:-1] + #passthrough options.
              ["-b:v", f"{bitrate:.0f}k",
              "-maxrate", f"{bitrate*4:.0f}k",
              "-b:a", "64k",
              sys.argv[-1]]) # output filename
          
              
    print (" ".join(command))
    result = subprocess.run(command)   
       
    delete_logs()
    return os.path.getsize(sys.argv[-1])
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print (f"usage: {sys.argv[0]} <regular ffmpeg commands>")
        
    i_index = get_index(["-i", "-I"],sys.argv)
    if i_index is None:
        print("'-i' not found")
        sys.exit()
    
    filename = sys.argv[i_index+1]    
    print(f"Getting file:{filename}")
    length = get_length(filename)
    print(f"File length:{length} seconds")
        
    print(f"estimated audio size:, {AUDIO_RATE*length/8}KB")
        
    target_size = TARGET_SIZE
    actual_size = generate_file(target_size)
    print (actual_size, 7.5*1024*1024)
    
    if actual_size < MIN_SIZE_BYTES:
        print("For some reason we got a REALLY low file size.")
        target_size *= FULL_SIZE_BYTES/actual_size
        actual_size = generate_file(target_size)    
        
    while actual_size > FULL_SIZE_BYTES:
        print("Uh oh, we're still over size: ", actual_size/1024/1024.0)
        target_size -= 100
        actual_size = generate_file(target_size)
        