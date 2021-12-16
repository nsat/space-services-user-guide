# Getting Started

Consider reading about the [fundamentals](./Fundamentals.md) first - many of the concepts and terms are described.

## Prerequisites

Spire provides access to 1 or more satellites and payloads with a [Tasking API Authentication Token](https://developers.spire.com/tasking-api-docs/#authentication).  The API can be queried to see what assets are available:

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/satellites"
```

The example response below shows that the authentication token has access to [3 window types](https://developers.spire.com/tasking-api-docs/#supported-windows) on 1 satellite with id `FM142`:

```bash
{
  "data": [{
    "id": "FM142",
    "norad_id": "46926",
    "supported_windows": [
      "PAYLOAD_SDR",
      "PAYLOAD_SABERTOOTH",
      "CONTACT_SDR_IQ"
    ]
  }]
}
```

More information on this endpoint is available [here](https://developers.spire.com/tasking-api-docs/#select-satellite)

## Start Here

 - [**Hello World Tutorial**](./tutorials/hello_world/HelloWorld.md)
 - [Full list of tutorials](#tutorials)
 - [Understanding the Execution Environment](./ExecutionEnvironment.md)
 - [FAQ](./FAQ.md)


## Tutorials

 - [Hello World](./tutorials/hello_world/HelloWorld.md)
 - [RF Collect](./tutorials/rf_collect/RfCollect.md)
 - [RF Transmit](./tutorials/rf_transmit/RfTransmit.md)
 - [Scheduling over an area of interest](./tutorials/aio_scheduling/AoiScheduling.md)
 



