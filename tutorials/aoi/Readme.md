# Tracking an Area Of Interest Tutorial

|Complexity:|Medium|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

A satellite is useful for its ability to be over a specific area of interest (AOI). This tutorial will demonstrate how to determine at what time a window needs to be scheduled to be over an AOI, i.e. for observations or communications. These results can be compared with a site like [n2yo.com⤴](https://www.n2yo.com/passes/?s=46926) which provides transit information.

This example requires the [satellites Two-Line-Element (TLE)⤴](https://en.wikipedia.org/wiki/Two-line_element_set), which provides the satellite's location and velocity and which is needed to calculate transits over an AOI. It can be obtained from a range of places including [tle.spire.com⤴](http://tle.spire.com/).

The TLE requires the Norad Catalog Number (Norad Id).


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../GettingStarted.md#execution-environment-setup). For this tutorial Python 3.6+ & the `pypredict` python module is used (on the ground only).

### pypredict

Install the [`pypredict`⤴](https://github.com/nsat/pypredict) python module:

```bash
python3 -m pip install git+https://github.com/nsat/pypredict.git
```

## Norad Catalog Number

The Norad Catalog Number (Norad Id) is needed to to look up the TLE. It can be looked up from a range of websites, i.e. [n2yo.com⤴](https://www.n2yo.com/). Spire also provides this information - the Tasking API returns the Norad Id of satellites available to the user:

<aside class="notice">Replace [YOUR_AUTH_TOKEN] as needed.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"

curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/satellites"
```

The result shows that windows can be scheduled on `FM1` which has Norad Id `46926`:

```json
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

## TLE

We can take a look at the [TLE⤴](https://en.wikipedia.org/wiki/Two-line_element_set) of this satellite at any time by visiting [`http://tle.spire.com/46926`⤴](http://tle.spire.com/46926). Notice that the Norad Id is appended to the URL:

```bash
$ curl http://tle.spire.com/46926
0 LEMUR 2 DJARA
1 46926U 98067RW  21349.43520370  .00268022  00000-0  88734-3 0  9993
2 46926  51.6363 130.1765 0006706 333.8750  26.1916 15.89079723 63302
```

## Finding a Transit Time

This tutorial has an accompanying script called [`find_transit`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/aoi/find_transit). It relies on the [`pypredict`⤴](https://github.com/nsat/pypredict) python module.

```bash
usage: find_transit [-h] [--sat SAT] [--lat LAT] [--lon LON] [--alt ALT]
                    [--min MIN] [--hours HOURS]

Find transit times over lat,lon. Default LEMUR1 & San Francisco @ 30
degrees

optional arguments:
  -h, --help     show this help message and exit
  --sat SAT      Satellite norad id (default: 40044)
  --lat LAT      AOI latitude (default: 37.771034)
  --lon LON      AOI longitude (non-negative) (default: -122.413815)
  --alt ALT      AOI altitude, in meters (default: 0)
  --min MIN      Min elevation, in degrees (default: 30)
  --hours HOURS  Hours to search (default: 48)
  ```

Any non-json output is written to `stderr` and can be discarded with `2>/dev/null` if needed. The exit code (`$?`) is non-zero if no transits are found. Searching for an 80+ degree overhead transit of San Francisco (the default) in the next week would look like:

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

PyPredict returns [substantially more data⤴](https://github.com/nsat/pypredict#usage) than [`find_transit`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/aoi/find_transit) outputs - it is not needed for this tutorial.


### Interpreting the Data

The transit's start and end times are from horizon to horizon, giving a total duration of 773 seconds. Often the most useful part of the transit is at higher elevation where there is less atmosphere and the satellite is closer to the ground. We will take 360 second window with the peak in the middle, i.e. 180s before peak elevation, `1639709333`.


## Scheduling a Window

Task the satellite to track the San Francisco location `(37.771034, -122.413815)` using `adcs_config`, and start the `SDR` and make a 10 second capture of S-BAND for down-link:


<aside class="notice">Replace [YOUR_START] with the `start` result of `find_transit`, and [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
START=YOUR_START
DURATION=360
SAT_ID="YOUR_SAT_ID"

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
        "adcs_config": {
            "mode": "TRACKING",
            "aperture": "SBAND_SDR",
            "target_latitude_north": 37.771034,
            "target_longitude_east": -122.413815
        },        
        "user_command": {
            "executable": "/persist/bin/entry.sh",
            "executable_arguments": [
                "rfcollect",
                "-w", "/outbox/rf_collect.iq",
                "-o", "-l", "0"
            ]
        }
    }
}
EOF
```

## Review

Once the window has completed and enough time has passed for the IQ file to download, it can be reviewed in AWS S3 (see [Hello World tutorial](../hello_world/#review)).


## Next Steps

 - [Real-Time Attitude Control Tutorial](../adcs-lease/)
