# Inter-Payload Communications Tutorial

|Complexity:|Medium|
|-|-|
|Payloads:|`SDR` & `SABERTOOTH`|
|Windows:|`PAYLOAD_SDR` `PAYLOAD_SABERTOOTH`|

This walk-through shows how to communicate between two payloads on a single satellite using HTTP over TCP/IP through the local ethernet.

1. Start an HTTP server on the `SDR`
1. Have `SABERTOOTH` request a file from the `SDR` using `curl`
1. Review

Only ports 10000 and above are available to connect & bind to. Only payloads with an overlapping window are reachable. 


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md).


## Deploy Script

The [`deploy`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/ipc/deploy) contains the following steps:

1. Schedules a `PAYLOAD_SDR` window to run a web server
1. Schedules a `PAYLOAD_SABERTOOTH` window to download a file from the SDR webserver


## Schedule PAYLOAD_SDR Window

The deploy script creates a window on the `SDR` to start the built-in `python` `HTTP Server` on port `10101` sharing the entire filesystem (since the command is run from `/`). Nothing needs to be uploaded since this already exists in `python`. The server is stopped at the end of the window before the payload shuts down. Run the accompanying [`deploy`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/ipc/deploy) script:


## Schedule a PAYLOAD_SABERTOOTH Window

Next, the script creates a window on the `SABERTOOTH` for 30 seconds later to make an HTTP request to download `/var/log/syslog` from the `SDR` to the `/outbox`. The IP address of the SDR is [`10.2.1.8`](../../ExecutionEnvironment.md#payload-specifications).


<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
$ ./deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID]
```


## Review

Once the windows have completed and enough time has passed for the file to download, we can review it in AWS S3:

```bash
$ aws s3 ls --recursive s3://user-s3-bucket/a/directory/FM1/downlink/

2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_sdr_syslog
```

## Next Steps

 - [Low-level Data Transfer API Tutorial](../data_xfr/) 
