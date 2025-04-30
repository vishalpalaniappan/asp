from constants import ASV_DEF, DLV_DEF
import subprocess
import sys

def clearAsvImage():
    try:
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
        cmd = ["docker", "rmi", DLV_DEF["IMAGE_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result)
        if result.returncode != 0:
            print(f'Failed to remove image: {DLV_DEF["IMAGE_NAME"]}')
            return False
        print("Removed DLV Image.")
        return True
    except Exception as e:
        print(f"Error when removing DLV image: {e}")
        return False

def main(argv):
    if (not clearAsvImage()):
        return -1
    
    if (not clearDlvImage()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))