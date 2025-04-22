## Queries

The following are a list of queries that the query server accepts.

### 1. Get Systems
This query returns all the systems in the database. 

#### Query
```
{
    "query":  "GET_SYSTEMS"
}
```
#### Response
The response to this query will be structured as follows:
```
{
    "queryType": "GET_SYSTEMS",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2"
    },
    "response":  <list of systems>
}
```
### 2. Get Programs
This query returns all the programs for a given system id and version.
#### Query
```
{
    "queryType": "GET_PROGRAMS",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2"
    }
}
```
#### Response
The response to this query will be structured as follows:
```
{
    "queryType": "GET_PROGRAMS",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2"
    },
    "response":  <list of programs>
}
```
### 3. Get Deployments
This query returns all the deployments for a given system id and version. 
#### Query
```
{
    "queryType": "GET_DEPLOYMENTS",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2"
    }
}
```
#### Response
The response to this query will be structured as follows:
```
{
    "queryType": "GET_DEPLOYMENTS",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2"
    },
    "response":  <list of deployment ids>
}
```
### 4. Get Traces
This query returns all the unique traces for a given system id and version.,
#### Query
```
{
    "queryType": "GET_TRACES",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2",
        "deploymentId": "127b22dc-a2c3-4b58-a27b-f3ff8ac3997b"
    }
}
```
#### Response
The response to this query will be structured as follows:
```
{
    "queryType": "GET_TRACES",
    "data": {
        "systemId": 1234,
        "systemVersion": "0.0.2",
        "deploymentId": "ff842dc3-92a4-4d0a-9a67-d27444f3f98f"
    },
    "response":  <list of traces>
}
```
## Malformed Queries
In the event that a required field is not available in the query, the response will indicate that an error has occurred and provide the reason for the error.
#### Example
```
{
    "queryType": "GET_DEPLOYMENTS",
    "data": {
        "systemVersion": "0.0.2"
    },
    "response": "Request does not contain a system id.",
    "error": true
}
```