import subprocess
import json

def doesContainerExist(name):
    cmd = ["docker", "ps", "-aq", "-f", f"name={name}"]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )

    return len(output.stdout) > 0

def doesImageExist(name):
    cmd = ["docker", "image", "inspect", name]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )

    images = json.loads(output.stdout)

    return len(images) > 0

def buildImage(imageName, dockerPath, srcPath):

    if not doesImageExist(imageName):
        cmd = [
            "docker",
            "build",
            "-t",
            imageName,
            "-f",
            dockerPath,
            srcPath
        ]
        subprocess.run(cmd)