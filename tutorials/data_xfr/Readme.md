# Low-level Data Transfer API Tutorial

|Complexity:|Low|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

> WARNING: Testing this code locally requires the installation of export controlled libraries. Contact Spire if access is required.

The `/outbox` is a simple way to get data to the ground, but does not provide fine-grained prioritization and expiration. The [Data Pipeline API](https://developers.spire.com/data-pipeline-docs/) and accompanying SDKs provided by the [Spire Linux Agent](https://developers.spire.com/spire-linux-agent-docs/) expose low-level controls. 

A common use is to reduce the priority & time-to-live (TTL) of debug logs and sample raw data, both of which is nice to have, but shouldn't be prioritized over other data, and shouldn't sit in queues for a long time filling up the satellite bus cache.

This tutorial demonstrates queueing low-priority data for download, with a short expiry. 


## Prerequisites

1. The same [Hello World tutorial prerequisites](../hello_world/)


## Schedule Execution

Schedule the `SDR` to run a `PAYLOAD_SDR` window in 24 hours, that sends the file `/var/log/syslog` to the ground on the `demo` topic. If the file is not downloaded within 24 hours, it can be discarded. 


```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
START=$(( `date -u +'%s'` + 86400 ))
DATA='{\"destination\":\"ground\",\"filepath\":\"/var/log/syslog\",\"topic\":\"demo\",\"options\":{\"reliable\":true,\"TTLParams\":{\"urgent\":0,\"bulk\":0,\"surplus\":86400}}}'

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SDR",
    "satellite_id": "FM1",
    "start": ${START},
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "/persist/bin/entry.sh",
            "executable_arguments": [
                "curl", "-XPOST", "-v",
                "-H", "Content-type: application/json",
                "-d", "${DATA}",
                "http://localhost:2005/sdk/v1/send_file"
            ]
        }
    }
}
EOF
```


## Review

It is 24 hours before the window runs, and may take up to 24 more hours until the low-priority file is downloaded. The file can be found in the customer AWS S3 bucket (see [Hello World tutorial](../hello_world/#review)).
