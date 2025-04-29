from constants import *
import subprocess

def clearContainers():
    cmd = ["docker", "rm", DLV_CONTAINER_NAME]
    subprocess.run(cmd)

    cmd = ["docker", "rm", ASV_CONTAINER_NAME]
    subprocess.run(cmd)

if __name__ == "__main__":
    clearContainers()