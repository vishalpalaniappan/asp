## Queries

The following are a list of queries that the query server accepts.

### 1. Get Systems
This query returns all the systems in the database. 

#### Query
```
{
    "queryType":  "GET_SYSTEMS"
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
        "deploymentId": "ff842dc3-92a4-4d0a-9a67-d27444f3f98f"
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

## Invalid System Information
In the event that the provided system information is invalid, it will result in the program trying to access a table that doesn't exist. This will result in a response with an error and a reason for the error.

#### Example
```
{
    "queryType": "GET_DEPLOYMENTS",
    "data": {
        "systemId": 134,
        "systemVersion": "0.0.2"
    },
    "error": true,
    "response": "Database error: no such table: 134_0.0.2_deployments"
}
```