import subprocess
import os, sys
from constants import ASV_DEF, DLV_DEF

def stopASV():
    print("Stopping ASV...")
    cmd = ["docker", "stop",  ASV_DEF["CONTAINER_NAME"]]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )    
    print("Stopped ASV service.")

def stopDLV():
    print("Stopping DLV...")
    cmd = ["docker", "stop",  DLV_DEF["CONTAINER_NAME"]]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )    
    print("Stopped DLV service.")

if __name__ == "__main__":
    stopASV()
    stopDLV()