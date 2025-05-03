import subprocess
import os, sys
from constants import ASV_DEF, DLV_DEF, DB_DEF, ASP_DEF, QUERY_HANDLER_DEF
from utils import isDockerInstalled, doesContainerExist


def stopContainer(container_name, service_name):
    '''
        Generic function to stop a container.
    '''
    print(f"\nStopping {service_name}...")
    
    isContainerLoaded = doesContainerExist(container_name)

    if not isContainerLoaded:
        print(f"{service_name} Container does not exist. No need to stop it.")
        return True

    cmd = ["docker", "stop", container_name]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)    
        if result.returncode != 0:
            print(f"Failed to stop {service_name} container: {result.stderr}")
            return False   
    except Exception as e:
        print(f"Error stopping {service_name} container: {str(e)}")
        return False
    
    print(f"Stopped {service_name} service.")
    return True


def stopASV():
    '''
        Stop the ASV container.
    '''
    return stopContainer(ASV_DEF["CONTAINER_NAME"], "ASV")

def stopDLV():
    '''
        Stop the DLV container.
    '''
    return stopContainer(DLV_DEF["CONTAINER_NAME"], "DLV")

def stopDB():
    '''
        Stop the DB container.
    '''
    return stopContainer(DB_DEF["CONTAINER_NAME"], "DB")

def stopASP():
    '''
        Stop the ASP Container
    '''
    return stopContainer(ASP_DEF["CONTAINER_NAME"], "ASP")

def stopQueryHandler():
    '''
        Stop the query handler.
    '''
    return stopContainer(QUERY_HANDLER_DEF["CONTAINER_NAME"], "query handler")

def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not stopASV()):
        return -1
    
    if (not stopDLV()):
        return -1
    
    if (not stopDB()):
        return -1
    
    if (not stopASP()):
        return -1
    
    if (not stopQueryHandler()):
        return -1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))