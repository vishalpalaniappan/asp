from constants import ASV_DEF, DLV_DEF, DB_DEF, ASP_DEF
from utils import isDockerInstalled, doesContainerExist
import subprocess
import sys

def deleteAsvContainer():
    '''
        Deletes the ASV Container.
    '''
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
    
def deleteDlvContainer():    
    '''
        Deletes the DLV container.
    '''
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
    
def deleteDbContainers():  
    '''
        Delete the DB container.
    '''  
    try:
        isContainerLoaded = doesContainerExist(DB_DEF["CONTAINER_NAME"])

        if not isContainerLoaded:
            print("DB Container does not exist. No need to clear it.")
            return True

        cmd = ["docker", "rm", DB_DEF["CONTAINER_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f'Failed to remove container: {DB_DEF["CONTAINER_NAME"]}')
            return False
        
        print("Removed DB Container.")

        return True    
    except Exception as e:
        print(f"Error when removing DB container: {e}")
        return False
    
def deleteAspContainer():  
    '''
        Delete the ASP container.
    '''  
    try:
        isContainerLoaded = doesContainerExist(ASP_DEF["CONTAINER_NAME"])

        if not isContainerLoaded:
            print("ASP Container does not exist. No need to clear it.")
            return True

        cmd = ["docker", "rm", ASP_DEF["CONTAINER_NAME"]]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f'Failed to remove container: {ASP_DEF["CONTAINER_NAME"]}')
            return False
        
        print("Removed ASP Container.")

        return True    
    except Exception as e:
        print(f"Error when removing ASP container: {e}")
        return False

def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not deleteAsvContainer()):
        return -1
    
    if (not deleteDlvContainer()):
        return -1
    
    if (not deleteDbContainers()):
        return -1
    
    if (not deleteAspContainer()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))