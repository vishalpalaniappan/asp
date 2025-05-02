# Database Structure

### SYSTEM TABLE

Table Name: SYSTEMSTABLE

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|--------------------------------------------------:|
| system_id          |  STRING     | Unique System Id (eg 823642)                      |
| version            |  STRING     | Version of the system (eg "0.1")                  |
| name               |  STRING     | Name of the system (Distributed Sorting System)   |
| description        |  STRING     | Description of the system                         |
| programs           |  STRING     | JSON String representation of the file tree       |


### Deployments

Table Name: <sys_id>_<sys_ver>_deployments

| Column Name        |  Data Type     |  Description |
|--------------------|:--------------:|----------------------------:|
| deployment_id      |  VARCHAR(100)  | Deployment Id (eg 554233)   |
| startTs            |  TIMESTAMP     | Start of Trace              |
| endTs              |  TIMESTAMP     | End of Trace                |


### Traces

Table Name: <sys_id>_<sys_ver>_traces

| Column Name        |  Data Type       |  Description |
|--------------------|:----------------:|------------------------------------------------:|
| deployment_id      |  VARCHAR(100)    | Deployment Id (eg 554233)                       |
| trace_id           |  VARCHAR(100)    | Trace Id (eg 235234)                            |
| start_ts           |  TIMESTAMP       | Start of Trace                                  |
| end_ts             |  TIMESTAMP       | End of Trace                                    |
| trace_type         |  VARCHAR(100)    | Type of trace                                   |
| traces             |  TEXT            | JSON String of the traces for this program      |