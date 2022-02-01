# Low-level Data Transfer API Tutorial

|Complexity:|Low|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

The `/outbox` is a simple way to get data to the ground, but does not provide fine-grained prioritization and expiration. The [Data Pipeline API](https://developers.spire.com/data-pipeline-docs/) and accompanying SDKs provided by the [Spire Linux Agent](https://developers.spire.com/spire-linux-agent-docs/) expose low-level controls. 

A common use is to reduce the priority & time-to-live (TTL) of debug logs and sample raw data, both of which is nice to have, but shouldn't be prioritized over other data, and shouldn't sit in queues for a long time filling up the satellite bus cache.

This tutorial demonstrates queueing low-priority data for download, with a short expiry. 


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md). 


## Schedule Execution

Schedule the `SDR` to run a `PAYLOAD_SDR` window in 24 hours, that sends the file `/var/log/syslog` to the ground on the `demo` topic. If the file is not downloaded within 24 hours, it will be discarded. Take a look at [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy):


<aside class="notice">Replace [YOUR_AUTH_TOKEN], [YOUR_SAT_ID] as needed.</aside>

```bash
$ ./deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID]
```


## Review

After the windows completes and enough time is given for download, the file can be found in the user's AWS S3 bucket (see [Hello World tutorial](../hello_world/#review)).


## Next Steps

