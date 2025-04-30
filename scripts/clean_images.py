from constants import ASV_DEF, DLV_DEF
from utils import isDockerInstalled, doesImageExist
import subprocess
import sys

def clearAsvImage():
    try:
        if not doesImageExist(ASV_DEF["IMAGE_NAME"]):
            print(f"{ASV_DEF['IMAGE_NAME']} Image does not exist.")
            return True
        
        cmd = ["docker", "rmi", ASV_DEF["IMAGE_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result)
        if result.returncode != 0:
            print(f'Failed to remove image: {ASV_DEF["IMAGE_NAME"]}')
            return False
        print("Removed ASV Image.")
        return True
    except Exception as e:
        print(f"Error when removing ASV image: {e}")
        return False
    
def clearDlvImage():    
    try:
        if not doesImageExist(DLV_DEF["IMAGE_NAME"]):
            print(f"{DLV_DEF['IMAGE_NAME']} Image does not exist.")
            return True
        
        cmd = ["docker", "rmi", DLV_DEF["IMAGE_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f'Failed to remove image: {DLV_DEF["IMAGE_NAME"]}')
            return False
        print("Removed DLV Image.")
        return True
    except Exception as e:
        print(f"Error when removing DLV image: {e}")
        return False

def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not clearAsvImage()):
        return -1
    
    if (not clearDlvImage()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))