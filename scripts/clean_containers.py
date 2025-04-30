from constants import ASV_DEF, DLV_DEF
import subprocess

def clearContainers():
    cmd = ["docker", "rm", DLV_DEF["CONTAINER_NAME"]]
    subprocess.run(cmd)

    cmd = ["docker", "rm", ASV_DEF["CONTAINER_NAME"]]
    subprocess.run(cmd)

if __name__ == "__main__":
    clearContainers()