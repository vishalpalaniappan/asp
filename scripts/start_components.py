#! /usr/bin/env python3

import subprocess
from utils import doesContainerExist, buildImage
from constants import *
import os
import sys

def buildImages():
    buildImage(ASV_IMAGE_NAME, ASV_IMAGE_PATH, ASV_COMPONENT_PATH)
    buildImage(DLV_IMAGE_NAME, DLV_IMAGE_PATH, DLV_COMPONENT_PATH)


def createDirectories():
    os.makedirs("data", exist_ok=True)
    os.makedirs(ASV_DATA_DIR, exist_ok=True)
    os.makedirs(DLV_DATA_DIR, exist_ok=True)

def startASV():
    '''
        Starts the automated system viewer container.
    '''

    print("Starting Automated System Viewer...")

    if (doesContainerExist(ASV_CONTAINER_NAME)):
        cmd = ["docker", "start", ASV_CONTAINER_NAME]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to start ASV container: {result.stderr}")
            return False
    else:
        cmd = [
            "docker", "run",\
            "-d",\
            "--name", ASV_CONTAINER_NAME,\
            "-p", f"{ASV_PORT}:{ASV_PORT}", \
            "-v", "./data/asv:/app/dist", \
            ASV_IMAGE_NAME \
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to start ASV container: {result.stderr}")
            return False

    print(f"Started Automated System Viewer on port {ASV_PORT}.")

    return True

def startDLV():
    '''
        Starts the diagnostic log viewer container.
    '''

    print("Starting Diagnostic Log Viewer...")    

    if (doesContainerExist(DLV_CONTAINER_NAME)):
        cmd = ["docker", "start", DLV_CONTAINER_NAME]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to start DLV container: {result.stderr}")
            return False
    else:
        cmd = [
            "docker", "run",\
            "-d",\
            "--name", DLV_CONTAINER_NAME,\
            "-p", f"{DLV_PORT}:{DLV_PORT}", \
            "-v", "./data/dlv:/app/dist", \
            DLV_IMAGE_NAME \
        ]
        result = subprocess.run(cmd,capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to start DLV container: {result.stderr}")
            return False
        
    print(f"Started Diagnostic Log Viewer on port {DLV_PORT}.")

    return True


def main(argv):
    createDirectories()
    buildImages()
    
    if (not startASV()):
        return -1
    
    if (not startDLV()):
        return -1

if __name__ == "__main__":
    sys.exit(main(sys.argv))