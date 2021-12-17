# Inter-Payload Communications Tutorial

|Complexity:|Medium|
|-|-|
|Payloads:|`SDR` & `SABERTOOTH`|
|Windows:|`PAYLOAD_SDR` `PAYLOAD_SABERTOOTH`|

This walk-through shows how to communicate between two payloads on a satellite using HTTP over TCP/IP through the local ethernet.

1. Start an HTTP server on the `SDR`
1. Have `SABERTOOTH` request a file from the `SDR` using `curl`
1. Review

Only ports 10000 and above are available to connect to. Only payloads with an overlapping window are reachable. 


## Prerequisites

1. [Tasking API Authentication Token](https://developers.spire.com/tasking-api-docs/#authentication)
1. The `FM` number of a satellite with SDR & SABERTOOTH payloads
1. An AWS S3 bucket set up with Spire
1. `curl` or similar



## Schedule PAYLOAD_SDR Window

Create a window on the `SDR` to start the built-in `python` `HTTP Server` on port `10101` sharing the entire filesystem (since the command is run from `/`). Nothing needs to be uploaded since this already exists in `python`. The server is stopped at the end of the window before the payload shuts down.

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
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
            "executable": "python3",
            "executable_arguments": [
                "-m", "http.server", "10101", "--bind", "0.0.0.0"
        }
    }
}
EOF
```

## Schedule a PAYLOAD_SABERTOOTH Window

Next, create a window on the `SABERTOOTH` for 30 seconds later to make an HTTP request to download `/var/log/syslog` from the `SDR` to the `/outbox`. The IP address of the SDR is [`10.2.1.8`](../../ExecutionEnvironment.md#payload-specifications).


```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
START=$(( $START + 30 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SABERTOOTH",
    "satellite_id": "FM1",
    "start": ${START},
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "curl",
            "executable_arguments": [
                "http://10.2.1.8:10101/var/log/syslog", "-o", "/outbox/sdr_syslog"
        }
    }
}
EOF
```


## Review

Once the windows have completed and enough time has passed for the file to download, we can review it in AWS S3:

```bash
$ aws s3 ls --recursive s3://customer-s3-bucket/a/directory/FM1/downlink/

2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_sdr_syslog
```
