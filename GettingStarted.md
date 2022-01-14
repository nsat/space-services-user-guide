# Getting Started

Consider reading about the [fundamentals](./Fundamentals.md) first - many of the concepts and terms are described.


## Prerequisites

1. [Tasking API Authentication Token](https://developers.spire.com/tasking-api-docs/#authentication)
1. The `FM` number of a satellite with an SDR payload
1. An AWS S3 bucket set up with Spire
1. `curl` or similar

Spire provides access to 1 or more satellites and payloads with a [Tasking API Authentication Token](https://developers.spire.com/tasking-api-docs/#authentication).  The API can be queried to see what assets are available:

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/satellites"
```

The example response below shows that the authentication token has access to [3 window types](https://developers.spire.com/tasking-api-docs/#supported-windows) on 1 satellite with id `FM1`:

```bash
{
  "data": [{
    "id": "FM1",
    "norad_id": "46926",
    "supported_windows": [
      "PAYLOAD_SDR",
      "PAYLOAD_SABERTOOTH"
    ]
  }]
}
```

More information on this endpoint is available [here](https://developers.spire.com/tasking-api-docs/#select-satellite)

## Execution Environment Setup

The Tasking API is used to deploy apps to payloads and execute them. It is helpful to use a wrapper script to provide a consistent environment between payloads, to set common environment variables and capture `stdout` and `stderr` to a log file for download at the end of the window. More information about execution environment can be found [here](../ExecutionEnvironment.md#filesystem). The wrapper script, named [`entry.sh`](https://github.com/nsat/space-services-user-guide/blob/main/dev-env/entry.sh) should be deployed to each payload at `/persist/bin/entry.sh` and used for all execution commands. The script can be deployed with:


```bash
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SATELLITE_ID="satellite_id=FM1"

curl -o entry.sh "https://github.com/nsat/space-services-user-guide/blob/main/dev-env/entry.sh"
HOST="https://api.orb.spire.com"
DESTINATION_PATH="destination_path=/persist/bin/entry.sh"
EXECUTABLE="executable=true"
```

```bash
PAYLOAD="payload=SDR"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@entry.sh"
```

```bash
PAYLOAD="payload=SABERTOOTH"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@entry.sh"
```

```bash
PAYLOAD="payload=IPI"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@entry.sh"
```

All tutorials require `entry.sh` to be deployed.

## Tutorials

 - [Hello World](./tutorials/hello_world/)
 - [RF Collect](./tutorials/rf_collect/)
 - [RF Transmit](./tutorials/rf_transmit/)
 - [Tracking an Area Of Interest](./tutorials/aoi/)
 - [Inter-Payload Communications](./tutorials/ipc/)
 - [Low-level Data Transfer API](./tutorials/data_xfr/) 
