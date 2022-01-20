# Real-Time Attitude Control Tutorial

|Complexity:|High|
|-|-|
|Payloads:|`SDR` (any will do)|
|Windows:|`LEASE_ADCS` & `PAYLOAD_SDR`|

This tutorial demonstrates controlling the [Attitude Control and Determination System (ADCS)](../../AttitudeControl.md) from a payload. This tutorial follows on from the [Tracking an Area Of Interest Tutorial](../aoi/).

The ADCS can be controlled by user code from a payload while in orbit, using the [Satellite Bus API](https://developers.spire.com/satellite-bus-api/). This REST API is provided by the local [Spire Linux Agent](https://developers.sbox.spire.com/spire-linux-agent-docs/index.html#spire-linux-agent-introduction) (which is pre-installed on all Linux payloads), and has accompanying SDKs.


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](GettingStarted.md#execution-environment-setup). This tutorial should be completed after the [Tracking an Area Of Interest Tutorial](../aoi/#finding-a-transit-time).


## Finding a Transit Time

Use the [`find_transit`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/aoi/find_transit) script from [the last tutorial](../aoi/#finding-a-transit-time) to identify a time window where the satellite transits over an area of interest at a reasonable elevation. The example below is for satellite with Norad Id `46926` (`FM1`) and an elevation of 80 degrees, but consider reducing the elevation so that a transit can be found for between 24 and 48 hours in the future. 

```json
$ python3 find_transit --sat 46926 --min 80 --hours 168
2021-12-22 14:12:36.630581      773.389237      89.663970
[
    {
        "end": 1640183130.019818,
        "peak_elevation": 89.66397045560218,
        "peak_time": 1639709513.3850813,
        "start": 1640182356.6305811
    }
]
```


## Develop Script

The script [`track_realtime`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/adcs-lease/track_realtime) queries the API for current [ADCS](https://developers.spire.com/satellite-bus-api/index.html#adcs) & [TFRS](https://developers.spire.com/satellite-bus-api/index.html#tfrs) information, then requests the satellite to reorient the imaging aperture to track a specific point on the ground. ADCS is polled every second until the end of the window.


The API to command ADCS to track a target:

```python
    cmd = AdcsCommandRequest(command="TRACK", aperture="IPI", target=(lat, lon))
    res = agent.command_adcs(cmd)
```


Here the script is asserting that ADCS is still following the executed command. Since lat/lon coordinates are of type `float`, the values are compared with a margin of error of 1 degree (`LATLON_ERR_DEG`):

```python
def assert_tracking(hk, mode, lat, lon):
    if hk.acs_mode_active == mode \
        and abs(hk.latlontrack_lat - lat) < LATLON_ERR_DEG \
        and abs(hk.latlontrack_lon - lon) < LATLON_ERR_DEG:
```


Dump the ADCS telemetry to a file in the `/outbox`, in JSON format:

```python
    with open("/outbox/adcs_data.json", "a") as f:
...
        f.write(json.dumps(adcs.hk))
```

## Deploy Script

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SAT_ID="YOUR_SAT_ID"

SATELLITE_ID="satellite_id=${SAT_ID}"
PAYLOAD="payload=SDR"
DESTINATION_PATH="destination_path=/persist/bin/track_realtime"
EXECUTABLE="executable=true"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"

curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@track_realtime"
```


## Schedule ADCS Lease

<aside class="notice">Replace [YOUR_START] & [YOUR_END] with the `start` and `end` results of `find_transit`</aside>

```bash
START=YOUR_START
END=YOUR_END
DURATION=$((${END} - ${START}))
SAT_ID="YOUR_SAT_ID"

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "LEASE_ADCS",
    "satellite_id": "${SAT_ID}",
    "start": ${START},
    "duration": ${DURATION}
}
EOF
```

## Schedule Payload Window

```bash
curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SDR",
    "satellite_id": "${SAT_ID}",
    "start": ${START},
    "duration": ${DURATION},
    "parameters": {
        "user_command": {
            "executable": "/persist/bin/entry.sh",
            "executable_arguments": [
                "/persist/bin/track_realtime",
                "${END}",
                "37.771034", -122.413815"
            ]
        }
    }
}
EOF
```


# Review

Once the windows complete and the results are downlinked to AWS S3, they can be analyzed. 


## Next Steps

 - [Inter-Payload Communications Tutorial](./tutorials/ipc/)
