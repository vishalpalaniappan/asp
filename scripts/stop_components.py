import subprocess
import os, sys
from constants import ASV_DEF, DLV_DEF

def stopASV():
    '''
        Stop the ASV container.
    '''
    print("Stopping ASV...")

    cmd = ["docker", "stop",  ASV_DEF["CONTAINER_NAME"]]
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )

    if result.returncode != 0:
        print(f"Failed to stop ASV container: {result.stderr}")
        return False    
    
    print("Stopped ASV service.")
    return True

def stopDLV():
    '''
        Stop the DLV container.
    '''
    print("Stopping DLV...")
    
    cmd = ["docker", "stop",  DLV_DEF["CONTAINER_NAME"]]
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )    

    if result.returncode != 0:
        print(f"Failed to stop DLV container: {result.stderr}")
        return False   
    
    print("Stopped DLV service.")
    return True

def main(argv):
    if (not stopASV()):
        return -1
    
    if (not stopDLV()):
        return -1

if __name__ == "__main__":
    sys.exit(main(sys.argv))