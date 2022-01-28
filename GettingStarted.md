# Getting Started

This guide walks through setting up the user's [development environment](./dev-env/), the satellite payload's [execution environment](./ExecutionEnvironment.md), and introduces the user to the platform through [tutorials](./tutorials/).

Consider reading about the [fundamentals](./Fundamentals.md) first - many of the concepts and terms are described.


## Prerequisites

1. [Tasking API Authentication Token⤴](https://developers.spire.com/tasking-api-docs/#authentication)
   1. Contact your program’s technical point of contact to request one
1. Your company's AWS S3 bucket that was set up with Spire
1. The `FM` number of a satellite (Satellite Id) with an SDR payload (read on)
1. `bash`, `curl`, `git`, `python3` & [`jq`⤴](https://stedolan.github.io/jq/)
1. [Development Environment Setup](./dev-env/)
1. [Execution Environment Setup](./ExecutionEnvironment.md)


This site includes the scripts described in the tutorials. Start by grabbing the code:

```bash
$ git clone --depth=1 https://github.com/nsat/space-services-user-guide.git
```

The next step is to query the Tasking API for which satellites & windows the [Authentication Token⤴](https://developers.spire.com/tasking-api-docs/#authentication) grants access to. The script [`get_sats`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/get_stats) in the [`tutorials`](https://github.com/nsat/space-services-user-guide/tree/main/tutorials) directory demonstrates this:

<aside class="notice">Replace [YOUR_AUTH_TOKEN] as needed.</aside>


```bash
$ tutorials/get_sats "[YOUR_AUTH_TOKEN]"
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

 - Ensure the [Execution Environment](./ExecutionEnvironment.md) has been set up
 - Start on the [Tutorials](./tutorials/)
