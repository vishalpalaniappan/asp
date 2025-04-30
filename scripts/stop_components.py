import subprocess
import os, sys
from constants import ASV_DEF, DLV_DEF
from utils import isDockerInstalled, doesContainerExist

def stopASV():
    '''
        Stop the ASV container.
    '''
    print("Stopping ASV...")
    
    isContainerLoaded = doesContainerExist(ASV_DEF["CONTAINER_NAME"])

    if not isContainerLoaded:
        print("ASV Container does not exist. No need to stop it.")
        return True

    cmd = ["docker", "stop",  ASV_DEF["CONTAINER_NAME"]]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to stop ASV container: {result.stderr}")
            return False    
    except Exception as e:
        print(f"Error stopping ASV container: {str(e)}")
        return False
    
    print("Stopped ASV service.")
    return True

def stopDLV():
    '''
        Stop the DLV container.
    '''
    print("Stopping DLV...")
    
    isContainerLoaded = doesContainerExist(DLV_DEF["CONTAINER_NAME"])

    if not isContainerLoaded:
        print("DLV Container does not exist. No need to stop it.")
        return True

    cmd = ["docker", "stop",  DLV_DEF["CONTAINER_NAME"]]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)    
        if result.returncode != 0:
            print(f"Failed to stop DLV container: {result.stderr}")
            return False   
    except Exception as e:
        print(f"Error stopping DLV container: {str(e)}")
        return False
    
    print("Stopped DLV service.")
    return True

def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not stopASV()):
        return -1
    
    if (not stopDLV()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))