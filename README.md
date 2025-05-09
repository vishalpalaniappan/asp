# Automated System Processor

Automated System Processor (ASP) is a free fully automated log based diagnostic tool for software systems. 

# Usage

> [!NOTE]  
> This workflow has been tested on a WSL distro running Ubuntu with Docker Desktop and Python3.9. It has also been tested on an EC2 instance running Ubuntu with docker installed. This workflow will continue to evolve as support for more platforms is added and more complete testing is performed.

After cloning the repo onto a machine running Ubuntu, enter the repo's folder and follow these steps to start the components:

### 1. Installing Dependencies

To install the dependencies, run:
```shell
./scripts/install-deps.sh
```
In addition to installing python and other useful libraries, this script also installs [task](https://taskfile.dev/) if it doesn't exist.

### 2. Starting the System

To start the system, run:
```shell
task start
```
This will build the docker images and start the containers to run the following:

| Component                  | URL                    | PORT |
|----------------------------|------------------------|------|
| Automated System Processor |                        |      |
| Diagnostic Log Viewer      | http://localhost:3011/ | 3011 |
| Automated System Viewer    | http://localhost:3012/ | 3012 |
| Query Handler              | ws://localhost:8765    | 8765 |
| Database                   |                        | 3306 |

It also sets up the network connection between the containers so the database can be queried.

Once the system is fully started, the Automated System Viewer will automatically open in the browser. You can also manually visit the URL provided above.

To process new system log files, add the logs to the system_logs folder. ASP monitors this folder to process and index any new system level traces.

### 3. Stopping the System

To stop the system, run:
```shell
task stop
```

This will stop all the containers.

### 4. Cleaning and Restarting

To fully clean and restart the system:
```shell
task clean-and-restart
```
This command deletes all the images and containers. It also deletes any data stored in the container (eg. database). 

Currently, it does not clear the system_logs folder. I did this because I primarily use the clean-and-restart task while developing and it was helpful for me to retain the logs.

# System Diagram
![image](https://github.com/user-attachments/assets/787c7b7b-fff1-48e8-8ae0-03973437dc84)

# How does it work?

This section is in being reworked because the information it had was outdated.

In the mean time, please see these PR's for some more insight:
[PR #22](https://github.com/vishalpalaniappan/asp-query-server/pull/22)
[PR #23](https://github.com/vishalpalaniappan/asp-query-server/pull/23),
[PR #25](https://github.com/vishalpalaniappan/asp-query-server/pull/25), 

In the current version of this program, the system_logs folder contains all the log files belonging to the current system. In the future, once CDL log files are ingested by CLP, the features CLP provides will be used to improve the performance of this system.
