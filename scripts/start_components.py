import subprocess
from utils import doesContainerExist, buildImage
from constants import *
import os

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
        subprocess.run(["docker", "start", ASV_CONTAINER_NAME])
    else:
        cmd = [
            "docker", "run",\
            "-d",\
            "--name", ASV_CONTAINER_NAME,\
            "-p", f"{ASV_PORT}:{ASV_PORT}", \
            "-v", "./data/asv:/app/dist", \
            ASV_IMAGE_NAME \
        ]
        subprocess.run(cmd)
    print("Started asv on port 3011.")

def startDLV():
    '''
        Starts the diagnostic log viewer container.
    '''

    print("Starting dlv...")    
    if (doesContainerExist(DLV_CONTAINER_NAME)):
        subprocess.run(["docker", "start", DLV_CONTAINER_NAME])
    else:
        cmd = [
            "docker", "run",\
            "-d",\
            "--name", DLV_CONTAINER_NAME,\
            "-p", f"{DLV_PORT}:{DLV_PORT}", \
            "-v", "./data/dlv:/app/dist", \
            DLV_IMAGE_NAME \
        ]
        subprocess.run(cmd)
    print("Started dlv on port 3011.")

if __name__ == "__main__":
    createDirectories()
    buildImages()
    startASV()
    startDLV()