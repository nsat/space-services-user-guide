# Example: IQ Capture and Compression

In this trivial example, we will create a PAYLOAD_SDR window to capture a signal, compress the resulting IQ file and downlink the compressed
file to our S3 bucket.  We will be using XZ Utils for compression.

The full specification for PAYLOAD_SDR windows (along with other window types) can be found in the Tasking API
documentation [here](https://developers.spire.com/tasking-api-docs/#supported-windows)

You can learn more about IQ components [here](https://en.wikipedia.org/wiki/In-phase_and_quadrature_components#IQ_phase_convention)

## Assumptions

1. The lzma Python library is installed on our payload sandbox
1. An S3 bucket was provisioned for user data, we'll be using the bucket name `example` for this exercise

## Software

### tasking.sh

**Execution Environment: Ground**
**Language: Bash**

Bash script responsible for uploading our `compress.py` script to our payload and creating a payload 
window using curl commands to the [Tasking API](https://developers.spire.com/tasking-api-docs/).

### compress.py

**Execution Environment: Payload**
**Language: Python**

Python script responsible for compressing the input file and persisting the compressed output file.
This script takes two parameters

1. `--input` The path of the file to compress.
1. `--output` The path compressed output file path.

## Workflow

**1. The tasking.sh script is executed from the customer's cloud environment to uplink our compress.py script 
and create the necessary payload window to run the script on our payload.**

At this point, we can call the `GET /tasking/windows` to check the status of our window.

```bash
curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/windows?satellite_id=FM200
```

Our response will look something like:

```json
{
  "data": [{
    "id": "5f7770a7984c4b30856a3a810c1b3e2f",
    "type": "PAYLOAD_SDR",
    "satellite_id": "FM200",
    "state": "PENDING_SYNC",
    "start": 1599503800,
    "duration": 60,
    "parameters": {
      "user_command": {
          "executable": "/usr/bin/compress",
          "executable_arguments": [
              "--input", "/inbox/capture.iq",
              "--output", "/outbox/output.txt"
          ]
       }
    }
  }]
}
```

Additionally, we can also check the status of our upload by calling `GET /tasking/uploads`.

```bash
curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/uploads
```

Our response will look like:

```json
{
  "data": [
    {
      "satellite_id": "FM200",
      "payload": "SDR",
      "destination_path": "compress.py",
      "executable": true,
      "status": "PENDING",
      "id": "71c92e3c57bc440ea89d76c94cdf387f",
    }]
}
```

On the next contact, the payload window will be synced with the satellite.  Additionally, our 
compress.py file will be uploaded to the satellite bus.  Note: for larger files this could take multiple contacts.

Calling `GET /tasking/windows` should now return a window with the status set to SYNCED

```json
{
  "data": [{
    "id": "5f7770a7984c4b30856a3a810c1b3e2f",
    "type": "PAYLOAD_SDR",
    "satellite_id": "FM200",
    "state": "SYNCED",
    "start": 1599503800,
    "duration": 60,
    "parameters": {
      "user_command": {
          "executable": "/usr/bin/compress",
          "executable_arguments": [
              "--input", "/inbox/capture.iq",
              "--output", "/outbox/output.txt"
          ]
       }
    }
  }]
}
```

If our `compress.py` script was successfully uploaded, calling `GET /tasking/uploads` should now return:

```json
{
  "data": [
    {
      "satellite_id": "FM200",
      "payload": "PAYLOAD_SDR",
      "destination_path": "compress.py",
      "executable": true,
      "status": "UPLOADED",
      "id": "71c92e3c57bc440ea89d76c94cdf387f",
    }]
}
```

If it was only partially uploaded, we would see at status of `UPLOADING`.

**3. During payload window execution**

1. Beginning at the start time specified when creating the PAYLOAD_SDR window, a signal capture will occur using the
parameters specied in the `capture_config` section of the window definition.  The capture will complete continue for the duration specified.
In our example, this would be 5 seconds.

2. Our `compress.py` script will be called following the capture with the arguments

    `--input=/inbox/capture.iq`
    
    `--output=/outbox/capture.iq.xz`
    
    The script will compress the input file and place the resulting compressed file in our outbox

**4. Following the end of the payload window**

Since we placed our file into the `/outbox` folder, the file will be automatically queued for download following the payload window.

Once the file is successfully downloaded to the ground, it will be placed in our S3 bucket and can be retrieved using:

`aws s3 cp s3://example/capture.iq.xz capture.iq.xz`
