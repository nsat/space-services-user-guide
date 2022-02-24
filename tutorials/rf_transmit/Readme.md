# RF Transmit Tutorial

|Complexity:|Moderate|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

This tutorial will demonstrate creating and sending a waveform through the S-BAND radio on the `SDR` using the [`iqgenerator`](../../Utilities.md#iq-generator) and [`rftransmit`](../../Utilities.md#rf-transmit) utilities, and finally downloading a log of the activities.

*NOTE:* Receiving the transmitted waveform is beyond the scope of this tutorial as it requires a satellite dish controlled by the user.


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md).


## Overview

The tutorial comes with 2 scripts:

1. [`rf_transmit_demo`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/rf_transmit/rf_transmit_demo) - runs in-orbit on the SDR to demonstrate `rftransmit` running
1. [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/rf_transmit/deploy) - run by the user on the ground to upload `rf_transmit_demo` and schedule it to execute in a `PAYLOAD_SDR` window


## In-Orbit Script

A script has been created to run on the `SDR` Linux payload called [`rf_transmit_demo`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/rf_transmit/rf_transmit_demo). The script will generate an IQ file using the `iqgenerator` utility, then transmit it with the `rftransmit` utility.

Mark it executable and test it. An error message is expected as the utilities are not available on the ground.

```bash
chmod 755 rf_transmit_demo
./rf_transmit_demo
```

Output:

```bash
Tue Dec 14 05:20:03 UTC 2021
Linux 66891b47365c 5.10.16.3-microsoft-standard-WSL2 #1 SMP Fri Apr 2 22:23:49 UTC 2021 x86_64 Linux
./rf_transmit_demo: line 6: iqgenerator: not found
iqgenerator error: 127
./rf_transmit_demo: line 7: rftransmit: not found
rftransmit error: 127
```


## Deploy

The `rf_transmit_demo` script is uploaded and scheduled to run by using the [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/rf_transmit_demo/deploy) script:

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
$ ./deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID]
```

Response:

```json
...
{"data": {"id": "d25c7a43-b70d-4f57-81d5-ff5177b26158"}}
...
{"data": {"id": "3020553"}}
...
```

At this point the file has been queued for upload at the next possible contact, and a window scheduled to run it in 24 hours.  After `rf_transmit_demo` has run on the `SDR` the file file will be picked up by the satellite bus and queued for downlink to AWS S3.


## Review

After the windows completes and enough time is given for download, the the log file can be found in S3 with the timestamp appended to guarantee uniqueness:

```bash
aws s3 ls --recursive s3://user-s3-bucket/a/directory/${SAT_ID}/downlink/

2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_rf_transmit.log
```

Receiving the transmitted waveform is beyond the scope of this tutorial as it requires a receiver to be listening.


## Next Steps

 - [Tracking an Area Of Interest Tutorial](../aoi/)
