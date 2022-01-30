# RF Collect Tutorial

|Complexity:|Easy|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

This tutorial will demonstrate receiving signals from the S-BAND radio on the `SDR` using the [`rfcollect`](../../Utilities.md#rf-collect) utility, and download the produced [`IQ`⤴](https://en.wikipedia.org/wiki/In-phase_and_quadrature_components) and log files. The frequency can be changed to capture specific signals. 


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](GettingStarted.md#execution-environment-setup).

## Overview

The tutorial comes with 2 scripts:

1. [`rf_collect_demo`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/rf_collect/rf_collect_demo) - runs in-orbit on the SDR to demonstrate `rfcollect` running
1. [`deploy`⤴](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/rf_collect/deploy) - run by the user on the ground to upload `rf_collect_demo` and schedule it to execute in a `PAYLOAD_SDR` window


## In-Orbit Script

A script has been created that will run on the `SDR` Linux payload called `rf_collect_demo`. The default options of `rfcollect` make a 10 second 1MHz wide sample of the 2.0225 GHz S-BAND spectrum with a sample rate of 1MHz. This produces a 4MB IQ file (16bit in-phase + 16bit quadrature (4 bytes per sample) @ 1MHz).


Mark it executable and test it. An error message is expected because `rfcollect` is likely not available.

```bash
chmod 755 rf_collect_demo
./rf_collect_demo
```

Output:

```bash
Tue Dec 14 05:20:03 UTC 2021
Linux 66891b47365c 5.10.16.3-microsoft-standard-WSL2 #1 SMP Fri Apr 2 22:23:49 UTC 2021 x86_64 Linux
rf_collect_demo: line 4: rfcollect: not found
rfcollect error: 127
```


## Deploy

The script can be uploaded and scheduled to run by using the [`deploy`]() script:

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
$ ./deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID] [YOUR_START]
```

Response:

```json
{"data": {"id": "d25c7a43-b70d-4f57-81d5-ff5177b26158"}}
```

At this point the file has been queued for upload at the next possible contact. 



## Review

The files can be found in S3 with the timestamp appended to guarantee uniqueness. The `awscli` can be used with the `--recursive` option to see the files:

```bash
aws s3 ls --recursive s3://user-s3-bucket/a/directory/FM1/downlink/
```

Response:

```bash
2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_rf_collect.log
2021-09-06 04:32:29    4000000 2021/09/06/20210906T043229Z_rf_collect.iq
```

The IQ file can be further analyzed using digital signal analysis (DSP). For example the file can be loaded in [Universal Radio Hacker⤴](https://github.com/jopohl/urh) to view the spectrum:

![Spectrum](../../images/spectrum.png)


## Next Steps

 - [RF Transmit Tutorial](../rf_transmit/)
