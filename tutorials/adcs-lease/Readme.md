# Real-Time Attitude Control Tutorial

|Complexity:|High|
|-|-|
|Payloads:|`SDR` (any will do)|
|Windows:|`LEASE_ADCS` & `PAYLOAD_SDR`|

This tutorial demonstrates controlling the [Attitude Control and Determination System (ADCS)](../../AttitudeControl.md) from a payload. This tutorial follows on from the [Tracking an Area Of Interest Tutorial](../aoi/).

The ADCS can be controlled by user code from a payload while in orbit, using the [Satellite Bus API](https://developers.spire.com/satellite-bus-api/). This REST API is provided by the local [Spire Linux Agent](https://developers.sbox.spire.com/spire-linux-agent-docs/index.html#spire-linux-agent-introduction) (which is pre-installed on all Linux payloads), and has accompanying SDKs.

## Find an Area Of Interest



## Deploy Script

The script queries the API for current [ADCS](https://developers.sbox.spire.com/satellite-bus-api/index.html#adcs) & [TFRS](https://developers.sbox.spire.com/satellite-bus-api/index.html#tfrs) information, then requests the satellite to reorient at a point on the 

## Schedule ADCS Lease


## Schedule Payload Window


# Review

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>


## Next Steps

 - [Inter-Payload Communications Tutorial](./tutorials/ipc/)
