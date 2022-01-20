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

The script [`track_realtime`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/adcs-lease/track_realtime) queries the API for current [ADCS](https://developers.spire.com/satellite-bus-api/index.html#adcs) & [TFRS](https://developers.spire.com/satellite-bus-api/index.html#tfrs) information, then requests the satellite to reorient the imaging aperture to track a specific point on the ground. ADCS is polled every 5 seconds until slewing has completed.


The API to command ADCS to track a target:

```python
    cmd = AdcsCommandRequest(command="TRACK", aperture="IPI", target=(lat, lon))
    res = agent.command_adcs(cmd)
```


Here the script is asserting that ADCS is still following the executed command. Since lat/lon coordinates are of type `float`, the values are compared with a margin of error, `LATLON_ERR_DEG`:

```python
def assert_tracking(hk, mode, lat, lon):
    if hk.acs_mode_active == mode \
        and abs(hk.latlontrack_lat - lat) < LATLON_ERR_DEG \
        and abs(hk.latlontrack_lon - lon) < LATLON_ERR_DEG:
```


As the satellite slews closer to the target, the `control_error_angle_deg` will decrease. When it stops decreasing then ADCS slewing has completed and the `control_error_angle_deg` can be treated as the pointing accuracy.

```python
    # poll for the attitude until reached or it stops moving
    while assert_tracking(adcs.hk, MODE< lat, lon) \
        and adcs.hk.control_error_angle_deg < last_err_angle:
```


## Schedule ADCS Lease


## Schedule Payload Window


# Review

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>


## Next Steps

 - [Inter-Payload Communications Tutorial](./tutorials/ipc/)
