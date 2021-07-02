import sys
import subprocess
import glob
import os

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
    
    audio_rate = 64
    print(f"estimated audio size:, {audio_rate*length/8}KB")
    
    bitrate = (8100*8 - audio_rate*length)/ length
    if bitrate < 0:
        print(f"Unfortunately there is not enough bits for video!")
        sys.exit()
        
    command = (["ffmpeg", "-y"] + sys.argv[1:-1] + 
              ["-threads", "8", "-speed", "4", "-row-mt", "1", "-tile-columns", "2",
              "-vsync", "cfr",
              "-b:v", f"{bitrate:.0f}k", "-minrate", f"{bitrate/2:.0f}k",
              "-maxrate", f"{bitrate*1.5:.0f}k", "-an",
              "-pass", "1", "-f", "mp4","NUL"])
              
    print (" ".join(command))
    result = subprocess.call(command)
    
    command = (["ffmpeg", "-y"] + sys.argv[1:-1] + 
              ["-b:v", f"{bitrate:.0f}k", "-minrate", f"{bitrate/2:.0f}k",
              "-threads", "8", "-speed", "2", "-row-mt", "1", "-tile-columns", "2",
              "-maxrate", f"{bitrate*1.5:.0f}k",
              "-b:a", "64k",              
              "-pass", "2", sys.argv[-1], "-y"])
              
    print (" ".join(command))
    subprocess.call(command)
       
    delete_logs()
    