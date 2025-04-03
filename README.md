# ASP
Automted System Processor (ASP) is a free fully automated log based diagnostic solution for software systems. See this section for more information on how it works.

> [!NOTE]  
> This repo is in development. The usage section of this repo will be updated when all the necessary features are packaged into the application. 

# Usage
To run this program, run the following command:
  ```shell
  python3 server.py
  ```
This will start a websocket server on port 8765. After connecting to the websocket server, you can send commands to interface with the system processor. 

# How does it work?

At its core, ASP leverages a new kind of logging called Diagnostic Logging to achieve its functionality. Diagnostic logging is a process in which the instructions, variables and exceptions of a program are logged. Unlike traditional logging which logs information that have to be aggregated to provide diagnostic and analytical insight, with diagnostic logging, the program itself becomes the diagnostic and analytics tool. This results in a fully automated log based diagnostic solution that can perform automated root cause analysis.

Practically, there are two issues which hinder the use of diagnostic logging. The size of the generated logs and the overhead incurred when logging the variables within the program itself.

To address the issue of log file size, ASP leverages a free log management tool named Compressed Log Processor(CLP), which is capable of compressing logs and searching the compressed logs without decompression. CLP provides libraries to efficiently compress the log files into an intermediate representation format and to further compress the log when it is archived. CLP applies data specific compression to the logged data and exploits any repetitiveness to improve its compression.

A system diagram is provided below:

![Simplified AQS System Diagram](docs/system_diagram2.jpg)

## Automated Diagnostic Log Injector

The Automated Diagnostic Log Injector (ADLI) tool is used to inject logs needed to capture the diagnostic information from the program. It uses Abstract Syntax Tree's (AST) to traverse the program and 


