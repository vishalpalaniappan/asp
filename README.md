# ASP-QUERY-SERVER
This websocket server handles queries from the Automated System Viewer to extract and filter through system level traces. 

> [!NOTE]  
> This repo is in development and there are core features being added and explored.

# Usage
To run this program, run the following command:
  ```shell
  python3 adli.py <source_path>
  ```
This will start a websocket server on port 8765. After connecting to the websocket server, you can send commands to interface with the system processor. 

Note: There are limited commands available right now, see PR #13 for example commands. The functionality will be expanded as the system is developed further.

# System Diagram
![Simplified AQS System Diagram](docs/system_diagram2.jpg)

# How does it work?

## System Processor
- The SystemProcessor class identifies all the log files which belong to the system (currently, they are in a known folder).
- It uses the Cdl class to extract the program execution data from each log file and gathers the unique traces from each program. 
- It processes each unique trace and assembles the sub-traces from each program in the order they appear.
- It groups unique traces if they start and end at the same location, these traces have the same **Trace Type**.
- It allows the traces to be queried by timestamp, specific variable value or by UID (this will evolve)
    
Note: I think that for a given **trace type**, there are specific variables associated with it, it would be great to allow the user to select the variable and filter the traces for a specific variable value (ex. specific user, specific job type)

## CDL Reader
The Cdl class uses the clp-ffi-py library to decompress the CDL file and extract the program execution data. Some of the data that is extracted are:
- Execution Sequence
- Call stack for a given position
- Variable Stack for a given position
- Exception Information
- Unique Traces

## Queries
Coming soon

In the current version of this program, the sample_system_logs folder contains all the log files belonging to the current system. In the future, once CDL log files are ingested by CLP, the features CLP provides will be used to improve the performance of this system.
