#!/usr/bin/env python3

import subprocess
from utils import doesContainerExist, buildImage
from constants import ASV_DEF, DLV_DEF
import os
import sys

def buildImages():
    '''
        Build the images if they haven't been created.
    '''
    try:
        buildImage(ASV_DEF["IMAGE_NAME"], ASV_DEF["IMAGE_PATH"], ASV_DEF["COMPONENT_PATH"])
        buildImage(DLV_DEF["IMAGE_NAME"], DLV_DEF["IMAGE_PATH"], DLV_DEF["COMPONENT_PATH"])
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
        return True
    except Exception as e:
        print(f"Failed to create directories: {e}")
        return False

def startASV():
    '''
        Starts the automated system viewer container.
    '''

    print("Starting Automated System Viewer...")

    try:
        containerExists = doesContainerExist(ASV_DEF["CONTAINER_NAME"])
    except Exception as e:
        print("Failed check to see if ASV container exists: {e}")
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
        "-v", "./data/asv:/app/dist", \
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
    print("Starting Diagnostic Log Viewer...")    

    try:
        containerExists = doesContainerExist(DLV_DEF["CONTAINER_NAME"])
    except Exception as e:
        print("Failed check to see if DLV container exists: {e}")
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
        "-v", "./data/dlv:/app/dist", \
        DLV_DEF["IMAGE_NAME"] \
    ]

    result = subprocess.run(cmd,capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to start DLV container: {result.stderr}")
        return False
        
    print(f'Started Diagnostic Log Viewer on port {DLV_DEF["PORT"]}.')

    return True


def main(argv):
    if (not createDirectories()):
        return -1
    
    if (not buildImages()):
        return -1
    
    if (not startASV()):
        return -1
    
    if (not startDLV()):
        return -1

if __name__ == "__main__":
    sys.exit(main(sys.argv))