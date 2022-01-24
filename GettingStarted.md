# Getting Started

This guide walks through setting up the user's [development environment](./dev-env/), the satellite payload's [execution environment](./ExecutionEnvironment.md), and introduces the user to the platform through [tutorials](./tutorials/).

Consider reading about the [fundamentals](./Fundamentals.md) first - many of the concepts and terms are described.


## Prerequisites

1. [Tasking API Authentication Token⤴](https://developers.spire.com/tasking-api-docs/#authentication)
   1. Contact your program’s technical point of contact to request one
1. The `FM` number of a satellite (Satellite Id) with an SDR payload (see [below](#satellite-ids))
1. Your company's AWS S3 bucket that was set up with Spire
1. `curl` or similar
1. [Development Environment Setup](./dev-env/)
1. [Execution Environment Setup](./ExecutionEnvironment.md)

### Satellite Ids

Spire provides access to 1 or more satellites and payloads with a [Tasking API Authentication Token⤴](https://developers.spire.com/tasking-api-docs/#authentication).  The API can be queried to see what assets are available:

<aside class="notice">Replace [YOUR_AUTH_TOKEN] as needed.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/satellites"
```

The example response below shows that the authentication token has access to [2 window types⤴](https://developers.spire.com/tasking-api-docs/#supported-windows) on 1 satellite with id `FM1`:

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

More information on this endpoint is available [here⤴](https://developers.spire.com/tasking-api-docs/#select-satellite)


## Next Steps

 - [Tutorials](./tutorials/)
