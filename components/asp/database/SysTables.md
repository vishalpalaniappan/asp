# Database Structure

### SYSTEM TABLE

Table Name: SYSTEMSTABLE

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|--------------------------------------------------:|
| system_id          |  STRING     | Unique System Id (eg 823642)                      |
| version            |  STRING     | Version of the system (eg "0.1")                  |
| name               |  STRING     | Name of the system (Distributed Sorting System)   |
| description        |  STRING     | Description of the system                         |
| programs           |  STRING     | JSON String representation of list of file names  |


### Deployments

Table Name: <sys_id>_<sys_ver>_deployments

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|------------------------------------------------:|
| deployment_id      |  STRING     | Deployment Id (eg 554233)                       |

### Programs

Table Name: <sys_id>_<sys_ver>_programs

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|------------------------------------------------:|
| name               |  STRING     | Name of Program                                 |
| description        |  STRING     | Description of program                          |
| language           |  STRING     | Language of the program (eg. python)            |
| fileTree           |  STRING     | JSON String of the filetree for the program     |


### Traces

Table Name: <sys_id>_<sys_ver>_traces

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|------------------------------------------------:|
| deployment_id      |  STRING     | Deployment Id (eg 554233)                       |
| trace_id           |  STRING     | Trace Id (eg 235234)                            |
| startTs            |  REAL       | Start of Trace                                  |
| endTs              |  REAL       | End of Trace                                    |
| traceType          |  STRING     | Type of trace                                   |
| traces             |  STRING     | JSON String of the traces for this program      |