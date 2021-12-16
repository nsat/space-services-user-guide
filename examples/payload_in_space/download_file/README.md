# Example: Create and Download a File in Space

In this trivial example, we will be creating a file onboard our payload and downloading it to our S3 bucket.
The filename will be specified during window creation and the file will simply contain the id of the window used for
execution.

The scripts for running this example are provided in this folder.  For production usage of the Payload in Space offering,
it is the responsibility of the customer to author these scripts (notably `payload_exec`).

## Assumptions

1. [payload_exec](./payload_exec) was installed during flight flash of the payload.
1. A Python3 interpreter was installed during flight flash of the payload
1. An S3 bucket was provisioned for user data, we'll be using the bucket name `example` for this exercise

## Software

Three files were created to complete this example task.

### payload_exec

**Execution Environment: Payload**
**Language: Python**

Python executable used to orchestrate operations during a contact window.

1. Accepting arguments passed by the Signaling API
1. Managing any files that were placed in the payloads inbox
1. Parsing the window configuration file for the current window
1. Executing our download_file.py script

Please see the [Signaling API documentation](https://developers.spire.com/payload-signaling-api-docs/) 
for more information on the expected arguments passed to this executable.

### download_file.py

**Execution Environment: Payload**
**Language: Python**

Python script responsible for creating our file to download and downloading the file via the OORT SDK.
This script takes two parameters

1. `-n` The name of the file to create.
1. `-w` The ID of the current window


### tasking.sh

**Execution Environment: Ground**
**Language: Bash**

Bash script responsible for uploading our [download_file.py](./download_file.py) script to our payload and creating a payload 
window using curl commands to the [Tasking API](https://developers.spire.com/tasking-api-docs/).

## Workflow

**1. The tasking.sh script is executed from the ground to uplink our download_file.py script and create the necessary 
window to run the script on our payload.**

At this point, we can call the `GET /tasking/windows` to check the status of our window.

```bash
curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/windows?satellite_id=FM200
```

Our response will look something like:

```json
{
  "data": [{
    "id": "3020553",
    "type": "PAYLOAD_MY_PAYLOAD_NAME",
    "satellite_id": "FM200",
    "state": "PENDING_SYNC",
    "start": 1599503800,
    "duration": 60,
    "parameters": {
      "executable": "download_file.py",
      "filename": "space.txt"
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
      "payload": "MY_PAYLOAD_NAME",
      "destination_path": "download_file.py",
      "executable": true,
      "status": "PENDING",
      "id": "d25c7a43-b70d-4f57-81d5-ff5177b26158",
    }]
}
```

On the next contact, the payload window will be synced with the satellite.  Additionally, our 
download_task.py file will be uploaded to the satellite bus.  Note: for larger files this could take multiple contacts.

Calling `GET /tasking/windows` should now return a window with the status set to SYNCED

```json
{
  "data": [{
    "id": "3020553",
    "type": "PAYLOAD_MY_PAYLOAD_NAME",
    "satellite_id": "FM200",
    "state": "SYNCED",
    "start": 1599503800,
    "duration": 60,
    "parameters": {
      "executable": "download_file.py",
      "filename": "space.txt"
    }
  }]
}
```

If our `download_file.py` script was successfully uploaded, calling `GET /tasking/uploads` should now return:

```json
{
  "data": [
    {
      "satellite_id": "FM200",
      "payload": "MY_PAYLOAD_NAME",
      "destination_path": "download_file.py",
      "executable": true,
      "status": "UPLOADED",
      "id": "d25c7a43-b70d-4f57-81d5-ff5177b26158",
    }]
}
```

If it was only partially uploaded, we would see at status of `UPLOADING`.

**2. Prior to the payload window (1-5 minutes before the start of the payload window)**

Note: In this example we will use `123` as the ID of our window, but in production operations it could be any integer.

Prior to the start of the window, the satellite bus will power on our payload and do the following operations

1. Place our [download_file.py](./download_file.py) on the payload at path `/signaling/inbox/download_file.py`, assuming the file
was successfully uploaded before the window start time.

1. Place a window configuration file at path `/signaling/window_configs/123.json`.  The contents of the file are shown below.

    ```json
    {
        "version": 1,
        "signal_parameters": {
            "tasking_parameters": {
                "executable": "download_file.py",
                "filename": "space.txt"
            }
        }
    }
    ```

1. Call [payload_exec](./payload_exec), located on our payload, with the argument `-e` (the configure flag). 

   `nohup /usr/bin/payload_exec -u john -e -w 123 &> /dev/null &`.

   Our payload_exec executable exits when it receives a configure command, so nothing will happen on the payload.

**3. During payload window execution**

At window start time the satellite bus will issue another signaling command to [payload_exec](./payload_exec), 
this time without the configure flag.

```
nohup /usr/bin/payload_exec -u john -w 123 -t 1611718292 &> /dev/null &`
```

[payload_exec](./payload_exec) will then executing the following operations:

1. Copy [download_file.py](./download_file.py) from the Signaling API inbox to a top level directory (`/user_exec`).
1. Load the window configuration JSON for the contact
1. Execute our [download_file.py](./download_file.py) script (now located at `/user_exec/download_file.py`) 
with arguments taken from the window configuration JSON.

`download_file.py` will:

1. Create a temporary file named `space.txt` with the window_id as the contents.
1. Send the file to the payloads local OORT Agent for download to the ground

**4. Following the end of the payload window**

OORT will attempt to download our `space.txt` file during the next contact opportunity.  The next contact could be up to five hours
after the end of the window.  Additionally, larger files can take multiple contacts to download.

Once the file is successfully downloaded to the ground, it will be placed in our S3 bucket and can be retrieved using:

`aws s3 cp s3://example/space.txt space.txt`
