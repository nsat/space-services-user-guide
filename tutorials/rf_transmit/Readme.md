# RF Transmit Tutorial

|Complexity:|Moderate|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

This tutorial will demonstrate creating and sending a waveform through the S-BAND radio on the `SDR` using the [`iqgenerator`](../../Utilities.md#iq-generator) and [`rftransmit`](../../Utilities.md#rf-transmit) utilities, and finally downloading a log of the activities.

*NOTE:* Receiving the transmitted waveform is beyond the scope of this tutorial. See the advanced [RF Tx/Rx Tutorial](../rf_txrx/RfTxRx.md).


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](GettingStarted.md#execution-environment-setup).


## Develop

Create a script that will run on the `SDR` Linux payload called `rf_transmit.sh`. Append the date and the system name to help diagnose any issues. The script will create an IQ file and transmit it.

```sh
#!/usr/bin/env sh
((

  date
  uname -a
  iqgenerator -f rf_transmit.iq -o -l 0 || echo "iqgenerator error: $?"
  rftransmit -w rf_transmit.iq -o -l 0 || echo "rftransmit error: $?"
  rm  rf_transmit.iq

) 2>&1 ) > /outbox/rf_transmit.log
```

Mark it executable and test it. An error message is expected but the script will complete with a log file produced.

```bash
chmod 755 rf_transmit.sh
mkdir /outbox
./rf_transmit.sh
cat /outbox/rf_transmit.log
```

Output:

```bash
Tue Dec 14 05:20:03 UTC 2021
Linux 66891b47365c 5.10.16.3-microsoft-standard-WSL2 #1 SMP Fri Apr 2 22:23:49 UTC 2021 x86_64 Linux
./rf_transmit.sh: line 6: iqgenerator: not found
iqgenerator error: 127
./rf_transmit.sh: line 7: rftransmit: not found
rftransmit error: 127
```


## Deploy

Upload the script via the [Tasking API](https://developers.spire.com/tasking-api-docs/#post-upload) to the `SDR` on the satellite. Please change `<FM>` to the satellite `id`, and `<token>` to the token provided by Spire.

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SAT_ID="YOUR_SAT_ID"

SATELLITE_ID="satellite_id=${SAT_ID}"
PAYLOAD="payload=SDR"
DESTINATION_PATH="destination_path=/persist/bin/rf_transmit.sh"
EXECUTABLE="executable=true"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"

curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@rf_transmit.sh"
```

Response:

```json
{"data": {"id": "d25c7a43-b70d-4f57-81d5-ff5177b26158"}}
```

At this point the file has been queued for upload at the next possible contact. 


## Wait

We can poll for the status of the upload with the following command, and wait until it changes from `PENDING` to `UPLOADING` then finally `UPLOADED`. 

```bash
curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/uploads
```

Response:

```json
{
  "data": [
    {
      "satellite_id": "FM1",
      "payload": "SDR",
      "destination_path": "/persist/bin/rf_transmit.sh",
      "executable": true,
      "status": "PENDING",
      "id": "d25c7a43-b70d-4f57-81d5-ff5177b26158",
    }
  ]
}
```


## Schedule Execution

Add a [`PAYLOAD_SDR`](https://developers.spire.com/tasking-api-docs/#payload_sdr) window to the schedule for in 24 hours (86400 seconds). 24 hours was chosen as it's the earliest time that the window will reliably sync to the satellite.

```bash
START=$(( `date -u +'%s'` + 21600 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SDR",
    "satellite_id": "${SAT_ID}",
    "start": ${START},
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "/persist/bin/entry.sh",
            "executable_arguments": ["/persist/bin/rf_transmit.sh"]
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
            "executable": "/persist/bin/rf_transmit.sh"
        }
    }
  }]
}
```

After `rf_transmit.sh` has run on the `SDR` the file file will be picked up by the satellite bus and queued for downlink to AWS S3.


## Analyze

The log file can be found in S3 with the timestamp appended to guarantee uniqueness:

```bash
aws s3 ls --recursive s3://user-s3-bucket/a/directory/FM1/downlink/

2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_rf_transmit.log
```

Receiving the transmitted waveform is beyond the scope of this tutorial as it requires a receiver to be listening.


## Next Steps

 - [Tracking an Area Of Interest Tutorial](./tutorials/aoi/)
