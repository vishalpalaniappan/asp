from constants import ASV_DEF, DLV_DEF, ASP_DEF, NET_DEF
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
    
def clearAspImage():    
    try:
        if not doesImageExist(ASP_DEF["IMAGE_NAME"]):
            print(f"{ASP_DEF['IMAGE_NAME']} Image does not exist.")
            return True
        
        cmd = ["docker", "rmi", ASP_DEF["IMAGE_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f'Failed to remove image: {ASP_DEF["IMAGE_NAME"]}')
            return False
        print("Removed ASP Image.")
        return True
    except Exception as e:
        print(f"Error when removing ASP image: {e}")
        return False
    
def clearNetworks():    
    try:
        cmd = ["docker", "network", "rm", NET_DEF["NETWORK_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Removed Network: {NET_DEF['NETWORK_NAME']}")
        return True
    except Exception as e:
        print(f"Error when removing network named: {NET_DEF['NETWORK_NAME']}")
        return False

def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not clearNetworks()):
        return -1
    
    if (not clearAsvImage()):
        return -1
    
    if (not clearDlvImage()):
        return -1
    
    if (not clearAspImage()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))