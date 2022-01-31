# Inter-Satellite Links Tutorial

|Complexity:|High|
|-|-|
|Payloads:|2 satellites with ISL: `SDR` & `SABERTOOTH`|
|Windows:|`LEASE_ISL`, `PAYLOAD_SDR` & `PAYLOAD_SABERTOOTH`|


Inter-Satellite Links (ISL) are enabled for some satellites. ISL links can be made between a single pair of satellites following the same orbit so that they can be in contact at any time, where there is little relative motion between them. Satellites that are in intermittent contact (i.e. when their orbits overlap) may also be used for ISL contacts, so long as their direction is similar enough for meaningful contact time as well as low doppler-shift.


To simplify calculating when to schedule the windows, for this example we will be assuming that the satellites are in synchronous orbit.


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md). Additionally the `zfec` python module must be installed on the payload. See the [In-Orbit Python Environment Setup
](../../dev-env/in-orbit/) instructions for more information.


## Scripts

1. [`deploy`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/isl/deploy) - run by the user on the ground to upload `isl_tx_demo` & `isl_rx_demo`, and schedule them to execute in a `PAYLOAD_SDR` window
1. [`isl_tx_demo`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/isl/isl_tx_demo) - Runs on the transmitting payload/satellite to send data
1. [`isl_rx_demo`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/isl/isl_rx_demo) - Runs on the receiving payload/satellite to receive data


## Upload & Deploy

The [`deploy`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/isl/deploy) script is run by the user and performs the following steps:

1. Uploads `isl_tx_demo` & `isl_rx_demo` scripts to the respective satellites
1. Schedules an ISL between 2 satellites in 24 hours
1. Schedules a `PAYLOAD_SDR` window to run on the transmitting satellite to send data
1. Schedule a `PAYLOAD_SDR` window to run on the receiving satellite to listen for & downlink data


<aside class="notice">Replace [YOUR_AUTH_TOKEN], [SAT_ID_TX] & [SAT_ID_RX] as needed.</aside>

```bash
$ ./deploy "[AUTH_TOKEN]" [SAT_ID_TX] [SAT_ID_RX]
```


## Schedule LEASE_ISL

The `LEASE_ISL` is used to configure a one-way ISL using the S-BAND radio, providing a simplex IP link between the satellites. In this example UDP is used for data transfer as the protocol has no return acknowledgment and ideal for simplex links.

A single call to the Tasking API creates a `LEASE_ISL` in both satellites. For this example satellites `FM1` and `FM2` are scheduled for 5 minutes. Everything is scheduled 24 hours out when there are no conflicts with existing down-link contact windows.


## Review

Once the window has completed and enough time has passed for the log to download, it can be reviewed in AWS S3 (see [Hello World tutorial](../hello_world/#review)).



## Next Steps

 - [SABERTOOTH CUDA Tutorial](../cuda/) 
