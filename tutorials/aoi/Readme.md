# Tracking an Area Of Interest Tutorial

|Complexity:|Medium|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

A satellite is useful for its ability to be over a specific area of interest (AOI). This tutorial will demonstrate how to determine at what time a window needs to be scheduled to be over an AOI, e.g. for observations or communications. These results can be compared with a site like [n2yo.com](https://www.n2yo.com/passes/?s=51099) which provides transit information.

This example requires the [satellites Two-Line-Element (TLE)](https://en.wikipedia.org/wiki/Two-line_element_set), which provides the satellite's location and velocity, which is needed to calculate each transit over an AOI. The TLE can be obtained from a range of places including [tle.spire.com](http://tle.spire.com/), and requires the satellites Norad Catalog Number (Norad Id).

## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md). For this tutorial Python 3.6+ & the `pypredict` python module are used (on the ground only).

### pypredict

Install the [`pypredict`](https://github.com/nsat/pypredict) python module:

```bash
python3 -m pip install git+https://github.com/nsat/pypredict.git
```

## Norad Catalog Number

The Norad Catalog Number (Norad Id) is needed to to look up the TLE. It can be looked up from a range of websites, e.g. [n2yo.com](https://www.n2yo.com/). Spire also provides this information - the Tasking API returns the Norad Id of satellites available to the user:

<aside class="notice">Replace [YOUR_AUTH_TOKEN] as needed.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"

curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/satellites"
```

The result shows that windows can be scheduled on `FM1` which has Norad Id `51099`:

```json
{
  "data": [{
    "id": "FM1",
    "norad_id": "51099",
    "supported_windows": [
      "PAYLOAD_SDR",
      "PAYLOAD_SABERTOOTH"
    ]
  }]
}
```

## TLE

The [TLE](https://en.wikipedia.org/wiki/Two-line_element_set) of this satellite can be fetched at any time by visiting [`http://tle.spire.com/51099`](http://tle.spire.com/51099). Notice that the Norad Id was appended to the URL:

```
$ curl http://tle.spire.com/51099
0 LEMUR 2 KRYWE
1 51099U 98067RW  21349.43520370  .00268022  00000-0  88734-3 0  9993
2 51099  51.6363 130.1765 0006706 333.8750  26.1916 15.89079723 63302
```

## Finding a Transit Time

This tutorial has an accompanying script called [`find_transit`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/aoi/find_transit). It relies on the [`pypredict`](https://github.com/nsat/pypredict) python module installed previously.

```
usage: find_transit [-h] [--sat SAT] [--lat LAT] [--lon LON] [--alt ALT]
                    [--min MIN] [--hours HOURS]

Find transit times over lat,lon. Default LEMUR1 over North Pacific Ocean and 30 degrees

optional arguments:
  -h, --help     show this help message and exit
  --sat SAT      Satellite norad id (default: 40044)
  --lat LAT      AOI latitude (default: 40.0)
  --lon LON      AOI longitude (non-negative) (default: -176.0)
  --alt ALT      AOI altitude, in meters (default: 0)
  --min MIN      Min elevation, in degrees (default: 30)
  --hours HOURS  Hours to search (default: 48)
  ```

[North Pacific Ocean: (40.0, -176.0)](https://www.google.com/maps/place/40%C2%B000'00.0%22N+176%C2%B000'00.0%22W)



Any non-json output is written to `stderr` and can be discarded with `2>/dev/null` if needed. The exit code (`$?`) is non-zero if no transits are found. Searching for an 80+ degree overhead transit of the North Pacific Ocean (the default) in the next week would look like:

```
$ python3 aoi/find_transit --sat 51099 --min 80 --hours 168
2022-03-02 23:56:25.492111	722.555646	85.360401
[
    {
        "end": 1646266108.0477574,
        "peak_elevation": 85.36040128316404,
        "peak_time": 1646265745.711503,
        "start": 1646265385.4921112
    }
]
```


### Interpreting the Data

The transit's start and end times are from horizon to horizon, giving a total duration of 723 seconds for this result. Often the most useful part of the transit is at higher elevation where there is less atmosphere and the satellite is closer to the AOI. For this tutorial a 360 second window will be used, with the peak in the middle, 180s before peak elevation: `1646265383` epoch seconds.


## Scheduling a Window

Task the satellite to track a North Pacific Ocean location `(40.0, -176.0)` by specifying this location in the `adcs_config` section of the JSON in the API request, and start the `SDR` and make a 10 second capture of S-BAND for down-link. Take a look at [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy)


<aside class="notice">Replace [YOUR_START] with the calculated result of `find_transit`, and [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
$ ./deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID] [YOUR_START]
```

## Review

Once the window has completed and enough time has passed for the IQ file to download, it can be reviewed in AWS S3 (see [Hello World tutorial](../hello_world/#review)).


## Next Steps

 - [Real-Time Attitude Control Tutorial](../adcs-lease/)
