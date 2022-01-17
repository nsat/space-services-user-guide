# Getting Started

Consider reading about the [fundamentals](./Fundamentals.md) first - many of the concepts and terms are described.

TODO: add intro about what we're gonna do here, including tutorials.


## Prerequisites

1. [Tasking API Authentication Token](https://developers.spire.com/tasking-api-docs/#authentication)
1. The `FM` number of a satellite with an SDR payload
1. An AWS S3 bucket set up with Spire
1. `curl` or similar
1. [Development Environment Setup](./dev-env/)
1. [Execution Environment Setup](./ExecutionEnvironment.md)

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


## Next Steps

 - [Tutorials](./Tutorials.md)
