# Automated System Processor

Automated System Processor (ASP) is a free fully automated log based diagnostic tool for software systems. 

> [!NOTE]  
> This repo is in development and there are core features being added.

# Usage
Currently, each program has to be run separately. This workflow will be automated once core functionality is fully developed.

To run the query handler, go to components/query_handler and run:
  ```shell
  python3 server.py
  ```
This will start a websocket server on port 8765. After connecting to the websocket server, you can send commands to query the systems.

To run the system processor, go to components/asp and run:
  ```shell
  python3 SystemProcessor.py
  ```
This will process all the log files in the system_logs folder and index them to the database. Once ASV is developed, the information in the database can be visualized. 

# System Diagram
![image](https://github.com/user-attachments/assets/787c7b7b-fff1-48e8-8ae0-03973437dc84)

# How does it work?

This section is in being reworked because the information it had was outdated.

In the mean time, please see these PR's for some more insight:
[PR #22](https://github.com/vishalpalaniappan/asp-query-server/pull/22)
[PR #23](https://github.com/vishalpalaniappan/asp-query-server/pull/23),
[PR #25](https://github.com/vishalpalaniappan/asp-query-server/pull/25), 

In the current version of this program, the system_logs folder contains all the log files belonging to the current system. In the future, once CDL log files are ingested by CLP, the features CLP provides will be used to improve the performance of this system.
