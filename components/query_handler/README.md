## Query Path

1. A websocket server receives messages from a client. 
2. The query is handled by receiveMessage in queryHandler.py.
3. The query is passed to the handleQuery in queryHandler.py.
4. The query is processed by calling the relevant function from queryFunctions.py (database operations are performed using SystemDatabaseReader class instance).
5. The query result is sent back to the user.

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
    "response":  <list of systems with id, version, deployments and programs>
}

### 2. Get Traces
This query returns all the unique traces for a given system id and version, and deployment id.

Note: A feature to filter by time range will be added in a coming PR.

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