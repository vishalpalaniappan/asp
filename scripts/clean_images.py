from constants import *
import subprocess

def clearContainers():
    cmd = ["docker", "rmi", DLV_IMAGE_NAME]
    subprocess.run(cmd)

    cmd = ["docker", "rmi", ASV_IMAGE_NAME]
    subprocess.run(cmd)


if __name__ == "__main__":
    clearContainers()