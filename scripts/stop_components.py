import subprocess
from constants import *

def stopDb():

    print("Stopping ASV...")
    cmd = ["docker", "stop",  ASV_CONTAINER_NAME]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )    
    print("Stopped ASV service.")

    print("Stopping DLV...")
    cmd = ["docker", "stop",  DLV_CONTAINER_NAME]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )    
    print("Stopped DLV service.")

if __name__ == "__main__":
    stopDb()