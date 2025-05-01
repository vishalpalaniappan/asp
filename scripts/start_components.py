#!/usr/bin/env python3

import subprocess
from utils import doesContainerExist, buildImage, isDockerInstalled
from constants import ASV_DEF, DLV_DEF, DB_DEF, ASP_DEF
import os
import sys

def buildImages():
    '''
        Build the images if they haven't been created.
    '''
    try:
        buildImage(ASV_DEF["IMAGE_NAME"], ASV_DEF["IMAGE_PATH"], ASV_DEF["COMPONENT_PATH"])
        buildImage(DLV_DEF["IMAGE_NAME"], DLV_DEF["IMAGE_PATH"], DLV_DEF["COMPONENT_PATH"])
        buildImage(ASP_DEF["IMAGE_NAME"], ASP_DEF["IMAGE_PATH"], ASP_DEF["COMPONENT_PATH"])
        return True
    except Exception as e:
        print(f"Failed to build images: {e}")
        return False

def createDirectories():
    '''
        Create the data directories mounted to the docker containers.
    '''
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs(ASV_DEF["DATA_DIR"], exist_ok=True)
        os.makedirs(DLV_DEF["DATA_DIR"], exist_ok=True)
        os.makedirs(ASP_DEF["DATA_DIR"], exist_ok=True)
        return True
    except Exception as e:
        print(f"Failed to create directories: {e}")
        return False

def startASV():
    '''
        Starts the automated system viewer container.
    '''

    print("\nStarting Automated System Viewer...")

    try:
        containerExists = doesContainerExist(ASV_DEF["CONTAINER_NAME"])
    except Exception as e:
        print(f"Failed check to see if ASV container exists: {e}")
        return False

    # Check if the container exists and start it
    if (containerExists):
        print("ASV container already exists.")
        result = subprocess.run(
            ["docker", "start", ASV_DEF["CONTAINER_NAME"]],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Failed to start ASV container: {result.stderr}")
            return False
        
        print(f'Started Automated System Viewer on port {ASV_DEF["PORT"]}.')
        return True
    
    # If the container doesn't exist run it.
    cmd = [
        "docker", "run",\
        "-d",\
        "--name", ASV_DEF["CONTAINER_NAME"],\
        "-p", f'{ASV_DEF["PORT"]}:{ASV_DEF["PORT"]}', \
        "-v", f"{os.path.abspath('./data/asv')}:/app/dist", \
        ASV_DEF["IMAGE_NAME"] \
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to start ASV container: {result.stderr}")
        return False

    print(f'Started Automated System Viewer on port {ASV_DEF["PORT"]}.')

    return True

def startDLV():
    '''
        Starts the diagnostic log viewer container.
    '''
    print("\nStarting Diagnostic Log Viewer...")    

    try:
        containerExists = doesContainerExist(DLV_DEF["CONTAINER_NAME"])
    except Exception as e:
        print(f"Failed check to see if DLV container exists: {e}")
        return False

    # If the container exists, start it and return.
    if (containerExists):
        print("DLV container already exists.")
        result = subprocess.run(
            ["docker", "start", DLV_DEF["CONTAINER_NAME"]],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Failed to start DLV container: {result.stderr}")
            return False
        
        print(f'Started Diagnostic Log Viewer on port {DLV_DEF["PORT"]}.')
        return True

    # If the container doesn't exist, run it.
    cmd = [
        "docker", "run",\
        "-d",\
        "--name", DLV_DEF["CONTAINER_NAME"],\
        "-p", f'{DLV_DEF["PORT"]}:{DLV_DEF["PORT"]}', \
        "-v", f"{os.path.abspath('./data/dlv')}:/app/dist", \
        DLV_DEF["IMAGE_NAME"] \
    ]

    result = subprocess.run(cmd,capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to start DLV container: {result.stderr}")
        return False
        
    print(f'Started Diagnostic Log Viewer on port {DLV_DEF["PORT"]}.')

    return True

def startDatabase():
    print("\nStarting Database...")    

    try:
        containerExists = doesContainerExist(DB_DEF["CONTAINER_NAME"])
    except Exception as e:
        print(f"Failed check to see if DB container exists: {e}")
        return False  

    # If the container exists, start it and return.
    if (containerExists):
        print("DB container already exists.")
        result = subprocess.run(
            ["docker", "start", DB_DEF["CONTAINER_NAME"]],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Failed to start DB container: {result.stderr}")
            return False
        
        print(f'Started Database on port {DB_DEF["PORT"]}.')
        return True  

    # If the container doesn't exist, run it.
    cmd = [
        "docker", "run",\
        "-d",\
        "--name", DB_DEF["CONTAINER_NAME"],\
        "-v", f"{os.path.abspath('./data/mariadb')}:/var/lib/mysql", \
        "-e", f"MARIADB_ROOT_PASSWORD={DB_DEF['DATABASE_PASSWORD']}", \
        "-e", f"MARIADB_DATABASE={DB_DEF['DATABASE_NAME']}", \
        "-p", f'{DB_DEF["PORT"]}:{DB_DEF["PORT"]}', \
        "mariadb:latest"
    ]

    result = subprocess.run(cmd,capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to start DB container: {result.stderr}")
        return False
        
    print(f'Started Database on port {DB_DEF["PORT"]}.')

    return True

def startASP():
    '''
        Starts the automated system processor container.
    '''
    print("\nStarting Automated System Processor...")    

    try:
        containerExists = doesContainerExist(ASP_DEF["CONTAINER_NAME"])
    except Exception as e:
        print(f"Failed check to see if ASP container exists: {e}")
        return False

    # If the container exists, start it and return.
    if (containerExists):
        print("ASP container already exists.")
        result = subprocess.run(
            ["docker", "start", ASP_DEF["CONTAINER_NAME"]],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Failed to start ASP container: {result.stderr}")
            return False
        
        print(f'Started Automated System Processor on port {ASP_DEF["PORT"]}.')
        return True

    # If the container doesn't exist, run it.
    cmd = [
        "docker", "run",\
        "-d",\
        "--name", ASP_DEF["CONTAINER_NAME"],\
        "-v", f"{os.path.abspath('data/asp')}:/app/mnt", \
        ASP_DEF["IMAGE_NAME"] \
    ]

    result = subprocess.run(cmd,capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to start ASP container: {result.stderr}")
        return False
        
    print(f'Started Automated System Processor on port {ASP_DEF["PORT"]}.')

    return True


def main(argv):
    if (not isDockerInstalled()):
        return -1
    
    if (not createDirectories()):
        return -1
    
    if (not buildImages()):
        return -1
    
    if (not startASV()):
        return -1
    
    if (not startDLV()):
        return -1
    
    if (not startDatabase()):
        return -1
    
    if (not startASP()):
        return -1
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))

    '''
    docker run -d \
  --name mariadb \
  -e MARIADB_ROOT_PASSWORD=my-secret-pw \
  -p 3306:3306 \
  mariadb:latest'''