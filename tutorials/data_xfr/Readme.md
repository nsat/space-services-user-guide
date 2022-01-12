# Managing Data Transfer

|Complexity:|Low|
|-|-|
|Payloads:|`SDR`|
|Windows:|`PAYLOAD_SDR`|

> WARNING: Testing this code locally requires the installation of export controlled libraries. Contact Spire if access is required.

The `/outbox` is a simple way to get data to the ground, but it does not provide fine-grained prioritization and expiration. The [Data Pipeline API](https://developers.spire.com/data-pipeline-docs/) and accompanying SDKs provided by the [Spire Linux Agent](https://developers.spire.com/spire-linux-agent-docs/) expose low-level controls that are demonstrated below. 

A common use is to reduce the priority & time-to-live (TTL) of debug logs and sample raw data, both of which is nice to have, but shouldn't be prioritized over other data, and shouldn't sit in queues for a long time filling up the satellite bus cache.

This tutorial demonstrates queueing low-priority data for download, with a short expiry. 


## Prerequisites

1. `TOPIC` string: provided by Spire
1. The same [Hello World prerequisites](../hello_world/)



## Develop

```
```


## Deploy


## Schedule Execution


## Review