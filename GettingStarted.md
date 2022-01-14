# Getting Started

Consider reading about the [fundamentals](./Fundamentals.md) first - many of the concepts and terms are described.

## Prerequisites

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

## Start Here

 - [**Hello World Tutorial**](./tutorials/hello_world/)
 - [Full list of tutorials](#tutorials)
 - [Understanding the Execution Environment](./ExecutionEnvironment.md)
 - [SABERTOOTH Setup](./dev-env/sabertooth/)
 - [FAQ](./FAQ.md)


## Tutorials

 - [Hello World](./tutorials/hello_world/)
 - [RF Collect](./tutorials/rf_collect/)
 - [RF Transmit](./tutorials/rf_transmit/)
 - [Tracking an Area Of Interest](./tutorials/aoi/)
 - [Inter-Payload Communications](./tutorials/ipc/)
 - [Low-level Data Transfer API](./tutorials/data_xfr/) 
