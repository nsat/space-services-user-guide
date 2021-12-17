# Hello World Tutorial

|Complexity:|Easiest|
|-|-|
|Payloads:|`SDR`|

This walk-through shows how to upload and run a script on a satellite. This example runs on the [`SDR`](), but could run equally well on any of the Linux payloads.

1. Develop Hello World script
1. Deploy script
1. Wait for the script to be uploaded
1. Schedule script to run
1. Wait for script to run & results downloaded
1. Review


## Prerequisites

1. [Tasking API Authentication Token](https://developers.spire.com/tasking-api-docs/#authentication)
1. The `FM` number of a satellite with an SDR payload
1. An AWS S3 bucket set up with Spire
1. `curl` or similar


## Develop

Create a script that will run on the `SDR` Linux payload called `hello_world.sh`:

```sh
#!/usr/bin/env sh

echo "hello world" > /outbox/hello_world.txt
uname -a >> /outbox/hello_world.txt
```

Mark it executable and test it:

```bash
chmod 755 hello_world.sh
mkdir /outbox
./hello_world.sh
cat /outbox/hello_world.txt
```

Output:

```bash
hello world
Linux 47d8b6948190 5.10.16.3-microsoft-standard-WSL2 #1 SMP Fri Apr 2 22:23:49 UTC 2021 x86_64 Linux
```


## Deploy

Upload the script via the [Tasking API](https://developers.spire.com/tasking-api-docs/#post-upload) to the `SDR` on the satellite. Please change `<FM>` to the satellite `id`, and `<token>` to the token provided by Spire.

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"

SATELLITE_ID="satellite_id=FM1"
PAYLOAD="payload=SDR"
DESTINATION_PATH="destination_path=/hello_world.sh"
EXECUTABLE="executable=true"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"

curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@hello_world.sh"
```

Response:

```json
{
    "satellite_id": "FM1",
    "payload": "SDR",
    "destination_path": "/hello_world.sh",
    "executable": true,
    "status": "PENDING",
    "id": "d25c7a43-b70d-4f57-81d5-ff5177b26158",
}
```

At this point the file has been queued for upload at the next possible contact. 


## Wait

We can poll for the status of the upload with the following command, and wait until it changes from `PENDING` to `UPLOADING` then finally `UPLOADED`.

```bash
curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/uploads
```

Response:

```json
{"data": {"id": "d25c7a43-b70d-4f57-81d5-ff5177b26158"}}
```


## Schedule Execution

Add a [`PAYLOAD_SDR`](https://developers.spire.com/tasking-api-docs/#payload_sdr) window to the schedule for in 6 hours. 6 hours was chosen as it's the earliest time that the window is likely run.

```bash
START=$(( `date -u +'%s'` + 21600 ))

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
            "executable": "/hello_world.sh"
        }
    }
}
EOF
```

Response:

```json
{"data": {"id": "3020553"}}
```


## Wait

Schedule synchronization can be polled by querying for upcoming windows. `state` will change from `PENDING_SYNC` to `SYNCED`.

```bash
SATELLITE_ID="satellite_id=FM1"
QUERY_PARAMS="${SATELLITE_ID}"

curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/windows?${QUERY_PARAMS}"
```

Response:

```json
{
  "data": [{
    "id": "3020553",
    "type": "PAYLOAD_SDR",
    "satellite_id": "FM1",
    "state": "PENDING_SYNC",
    "start": 1599503800,
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "/hello_world.sh"
        }
    }
  }]
}
```

After `hello_world.sh` has run on the `SDR` the output file will be picked up by the satellite bus and queued for downlink to AWS S3.


## Review

The file can be found in the pre-arranged AWS S3 bucket with the timestamp appended to guarantee uniqueness. The `awscli` can be used with the `--recursive` option to see the file:

```bash
$ aws s3 ls --recursive s3://customer-s3-bucket/a/directory/FM1/downlink/

2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_hello_world.txt
```
