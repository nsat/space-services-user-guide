# Getting Started

TODO: Blurb about working with payloads


## Prerequisites

1. [Tasking API Authentication Token](/tasking-api-docs/index.html#authentication)
1. The `FM` number of a satellite with an SDR payload
1. An AWS S3 bucket set up with Spire
1. `curl` or similar


## Hello World

This example runs a script on the [`SDR`](), but could run equally well on any of the Linux payloads.

1. Develop Hello World script
1. Deploy script
1. Wait for the script to be uploaded
1. Schedule script to run
1. Wait for script to run & results downloaded
1. Review


### Develop

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
> hello world<br>
> Linux 47d8b6948190 5.10.16.3-microsoft-standard-WSL2 #1 SMP Fri Apr 2 22:23:49 UTC 2021 x86_64 Linux


### Deploy

Upload the script via the [Tasking API](/tasking-api-docs/index.html#post-upload) to the `SDR` on the satellite. Please change `<FM>` to the satellite `id`, and `<token>` to the token provided by Spire.

```bash
HOST="https://test.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"

SATELLITE_ID="satellite_id=FM123"
PAYLOAD="payload=SDR"
DESTINATION_PATH="destination_path=/hello_world.sh"
EXECUTABLE="executable=true"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"

curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@hello_world.sh"
```

*TODO*: check this:
> `{
      "satellite_id": "FM123",
      "payload": "SDR",
      "destination_path": "/hello_world.sh",
      "executable": true,
      "status": "PENDING",
      "id": "71c92e3c57bc440ea89d76c94cdf387f",
    }` 

At this point the file has been queued for upload at the next possible contact. 


### Wait

We can check the status of the upload with the following command, and wait until it changes from `PENDING` to `UPLOADING` then finally `UPLOADED`.

```bash
curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/uploads
```

Response:
> `{
  "data": [
    {
      "satellite_id": "FM142",
      "payload": "SDR",
      "destination_path": "/hello_world.sh",
      "executable": true,
      "status": "PENDING",
      "id": "71c92e3c57bc440ea89d76c94cdf387f",
    }
  ]
}`


### Schedule Execution

Add a [`PAYLOAD_SDR`](/tasking-api-docs/index.html#payload_sdr) window to the schedule for in 6 hours. 6 hours was chosen as it's the earliest time that will likely run.

```bash
START=$(( `date -u +'%s'` + 21600 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SDR",
    "satellite_id": "FM123",
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
> `TODO`


### Wait

Schedule synchronization can be confirmed by querying for upcoming windows. `state` will change from `PENDING_SYNC` to `SYNCED`.

```bash
SATELLITE_ID="satellite_id=FM123"
QUERY_PARAMS="${SATELLITE_ID}"

curl -X GET -H "${AUTH_HEADER}" "${HOST}/tasking/windows?${QUERY_PARAMS}"
```

> `{
  "data": [{
    "id": "5f7770a7984c4b30856a3a810c1b3e2f",
    "type": "PAYLOAD_SDR",
    "satellite_id": "FM142",
    "state": "PENDING_SYNC",
    "start": 1599503800,
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "/hello_world.sh"
        }
    }
  }]
}`

After `hello_world.sh` has run on the `SDR` the output file will be picked up by the satellite bus and queued for downlink to AWS S3.


### Review

The file can be found in S3, i.e.:

```bash
aws s3 ls s3://mybucket/
```

> `TODO`

