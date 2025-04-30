from constants import ASV_DEF, DLV_DEF
from utils import isDockerInstalled, doesContainerExist
import subprocess
import sys

def clearAsvContainer():
    try:
        isContainerLoaded = doesContainerExist(ASV_DEF["CONTAINER_NAME"])

        if not isContainerLoaded:
            print("ASV Container does not exist. No need to clear it.")
            return True
        
        cmd = ["docker", "rm", ASV_DEF["CONTAINER_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f'Failed to remove container: {ASV_DEF["CONTAINER_NAME"]}')
            return False
        
        print("Removed ASV Container.")

        return True
    except Exception as e:
        print(f"Error when removing ASV container: {e}")
        return False
    
def clearDlvContainer():    
    try:
        isContainerLoaded = doesContainerExist(DLV_DEF["CONTAINER_NAME"])

        if not isContainerLoaded:
            print("DLV Container does not exist. No need to clear it.")
            return True

        cmd = ["docker", "rm", DLV_DEF["CONTAINER_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f'Failed to remove container: {DLV_DEF["CONTAINER_NAME"]}')
            return False
        
        print("Removed DLV Container.")

        return True    
    except Exception as e:
        print(f"Error when removing DLV container: {e}")
        return False

def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not clearAsvContainer()):
        return -1
    
    if (not clearDlvContainer()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))