import subprocess
import json

def doesContainerExist(name):
    '''
        Check if the given container exists.
    '''
    cmd = ["docker", "ps", "-aq", "-f", f"name={name}"]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )
    return len(output.stdout) > 0

def doesImageExist(name):
    '''
        Check if the given image exists.
    '''
    cmd = ["docker", "image", "inspect", name]
    output = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )
    images = json.loads(output.stdout)
    return len(images) > 0

def buildImage(imageName, dockerPath, srcPath):
    '''
        Build the image given the docker image and source path.
    '''
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

def isDockerInstalled():
    """
        Check if Docker is installed and accessible.
    """
    try:
        cmd = ["docker", "--version"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = (result.returncode == 0)
        if (success):
            print("Docker is installed and is accessible.")
            return True
        else:
            print("Docker is not installed. Please install docker and try again.")
            return False
    except Exception as e:
        print(f"Error when checking if docker exists: {e}")
        return False