# Real-Time Attitude Control Tutorial

|Complexity:|High|
|-|-|
|Payloads:|`SDR` (any will do)|
|Windows:|`LEASE_ADCS` & `PAYLOAD_SDR`|

This tutorial demonstrates controlling the [Attitude Control and Determination System (ADCS)](../../AttitudeControl.md) from a payload. This tutorial follows on from the [Tracking an Area Of Interest Tutorial](../aoi/).

The ADCS can be controlled by user code from a payload while in orbit, using the [Satellite Bus API⤴](https://developers.spire.com/satellite-bus-api/). This REST API is provided by the local [Spire Linux Agent⤴](https://developers.spire.com/spire-linux-agent-docs/index.html#spire-linux-agent-introduction) (which is pre-installed on all Linux payloads), and has accompanying SDKs.


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md#execution-environment-setup). This tutorial should be completed after the [Tracking an Area Of Interest Tutorial](../aoi/#finding-a-transit-time).


## Finding a Transit Time

Use the [`find_transit`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/aoi/find_transit) script from the [Tracking an Area Of Interest](../aoi/#finding-a-transit-time) tutorial to identify a time window where the satellite transits over an area of interest at a reasonable elevation. The example below is for satellite with Norad Id `46926` (`FM1`) and an elevation of 80 degrees, but consider reducing the elevation so that a transit can be found for between 24 and 48 hours in the future. 

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

The script [`track_realtime`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/adcs-lease/track_realtime) queries the API for current [ADCS⤴](https://developers.spire.com/satellite-bus-api/index.html#adcs) & [TFRS⤴](https://developers.spire.com/satellite-bus-api/index.html#tfrs) information, then requests the satellite to reorient the imaging aperture to track a specific point on the ground. ADCS is polled every second until the end of the window.


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

For example to view the pointing error over time, download the file and then click "Choose File" below to chart the `control_error_angle_deg` over time. A sample file can be downloaded [here](adcs_data.json)


<div style="padding:20px;">
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <input type="file" id="selectFiles" value="Import" /><br />
</div>
<div id="chart" style="width:auto; height:300px; padding:20px;"></div>
<script>

    function loadFile() {
        var files = document.getElementById('selectFiles').files;
        if (files.length <= 0) {
            return false;
        }
        var fr = new FileReader();
        fr.onload = function (e) {
            drawLineChart(JSON.parse(e.target.result));
        }
        fr.readAsText(files.item(0));
    }
    document.getElementById('selectFiles').onchange = loadFile;

    function drawLineChart(data) {
        var dt = new google.visualization.DataTable();
        dt.addColumn('datetime', 'Time');
        dt.addColumn('number', 'Pointing Error (Degrees)');

        for (const value of data) {
            dt.addRow([new Date(value.unix_timestamp * 1000), value.control_error_angle_deg]);
        }

        var options = {
            title: 'ADCS Pointing Error',
            hAxis: { format: 'HH:mm:ss' },
            legend: { position: 'bottom', textStyle: { color: '#555', fontSize: 14 } }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart'));
        chart.draw(dt, options);
    }
    google.charts.load('visualization', { packages: ['corechart'] });
</script>



## Next Steps

 - [Inter-Payload Communications Tutorial](../ipc/)
