from constants import ASV_DEF, DLV_DEF
import subprocess

def clearImages():
    cmd = ["docker", "rmi", ASV_DEF["IMAGE_NAME"]]
    subprocess.run(cmd)

    cmd = ["docker", "rmi", DLV_DEF["IMAGE_NAME"]]
    subprocess.run(cmd)


if __name__ == "__main__":
    clearImages()