# Copy Files Between Payloads Tutorial

|Complexity:|Easiest|
|-|-|
|Payloads:|`SABERTOOTH` & `SDR`|
|Windows:|`PAYLOAD_SABERTOOTH`|

This tutorial demonstrates how to schedule the transfer a file from one payload to another on a satellite. It makes use of the [`copy_from`](https://developers.spire.com/tasking-api-docs/#copy_from) parameter on the [`window`](https://developers.spire.com/tasking-api-docs/#supported-windows) object for the file copy remote source and local destination. This tutorial has no accompanying code - all commands are provided in the windows definition below.

<aside class="notice">This is not the only way to transfer a file. Users may also use IP networking (see <a href="../ipc/">Inter-Payload Communication Tutorial</a>).</aside>


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md).


## Steps

The scheduled window will:

1. Before window start:
   1. Power up the `SDR` payload
   1. Power up the `SABERTOOTH` payload
   1. Copy `SDR:/var/log/syslog` to `SABERTOOTH:/tmp/syslog`
   1. Power down the `SDR` payload
1. At window start:
   1. Run `/persist/bin/entry.sh`
   1. `/persist/bin/entry.sh` runs:
      1. `mv /tmp/syslog /outbox/sdr_syslog` for download to AWS S3
1. At window end 60 seconds later:
   1. Power down the `SABERTOOTH` payload


## Schedule Payload Window


<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] below.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SAT_ID="YOUR_SAT_ID"
START=$(( `date -u +'%s'` + 86400 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SABERTOOTH",
    "satellite_id": "${SAT_ID}",
    "start": ${START},
    "duration": 60,
    "parameters": {
        "copy_from": [
            {
                "src_payload": "SDR",
                "src_path": "/var/log/syslog",
                "dst_path": "/tmp/syslog"
            }
        ],
        "user_command": {
            "executable": "/persist/bin/entry.sh",
            "executable_arguments": [
                "mv", "/tmp/syslog", "/outbox/sdr_syslog"
                ]
        }
    }
}
EOF
```

Response:

```json
{"data": {"id": "d25c7a43-b70d-4f57-81d5-ff5177b26158"}}
```

At this point the file has been queued for upload at the next possible contact. 


## Review

Once the windows have completed and enough time has passed for the file to download, we can review it in AWS S3:

```bash
$ aws s3 ls --recursive s3://user-s3-bucket/a/directory/${SAT_ID}/downlink/

2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_sdr_syslog
```
