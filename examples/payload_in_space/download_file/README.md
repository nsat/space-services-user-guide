# Example: Create and Download a File in Space

In this trivial example, we will be creating a file onboard our payload and dowloaded it to our S3 bucket.
The filename will be specified during window creation and the file will simply contain the id of the window used for
execution.

## Assumptions

1. payload_exec was installed during flight flash of the payload
1. A Python3 interpreter was installed during flight flash of the payload
1. An S3 bucket was provisioned for user data, we'll be using the bucket name `example` for this exercise

## Software

### payload_exec

**Execution Environment: Payload**
**Language: Python**

Python executable used to orchestrate operations during a contact window.

1. Accepting arguments passed by the Signaling API
1. Managing any files that were placed in the payloads inbox
1. Parsing the window configuration file for the current window
1. Executing our download_file.py script

Please see the Signaling API documentation for more information on the expected arguments passed to this executable

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



## Workflow

**tasking.sh is executed from the ground to uplink our download_file.py script and create the necessary 
window to run the script on our payload.**

At this point, we can call the `GET /windows` to check the status of our window.

```bash
SATELLITE_ID="satellite_id=FM200"
QUERY_PARAMS="${SATELLITE_ID}"

curl -X GET -H "${AUTH_HEADER}" ${HOST}/tasking/windows?${QUERY_PARAMS}
```

Our response will look something like:

```json
{
  "data": [{
    "id": "5f7770a7984c4b30856a3a810c1b3e2f",
    "type": "PAYLOAD_MY_PAYLOAD_NAME",
    "satellite_id": "FM200",
    "state": "PENDING_SYNC",
    "start": 1599503800,
    "duration": 60∂,
    "parameters": {
      "executable": "download_file.py",
      "filename": "space.txt"
    }
  }]
}
```

Additionally, we can also check the status of our upload by calling `GET /uploads`.

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
      "id": "71c92e3c57bc440ea89d76c94cdf387f",
    }]
}
```

On the next contact, the payload window will be synced with the satellite.  Additionally, our 
download_task.py file will be uploaded to the satellite bus.  Note: for larger files this could take multiple contacts.

Calling `GET /windows` should now return a window with the status set to SYNCED

``json
```json
{
  "data": [{
    "id": "5f7770a7984c4b30856a3a810c1b3e2f",
    "type": "PAYLOAD_MY_PAYLOAD_NAME",
    "satellite_id": "FM200",
    "state": "SYNCED",
    "start": 1599503800,
    "duration": 60∂,
    "parameters": {
      "executable": "download_file.py",
      "filename": "space.txt"
    }
  }]
}
```

If our `download_file.py` script was successfully uploaded, calling `GET /uploads` should now return:

```json
{
  "data": [
    {
      "satellite_id": "FM200",
      "payload": "MY_PAYLOAD_NAME",
      "destination_path": "download_file.py",
      "executable": true,
      "status": "UPLOADED",
      "id": "71c92e3c57bc440ea89d76c94cdf387f",
    }]
}
```

If it was only partially uploaded, we would see at status of `UPLOADING`.

**Window start time is approaching**

Note: In this example we will use `123` as the ID of our window, but in production operations it could be any integer.

Prior to the start of the window, the satellite bus will power on our payload and do the following operations

1. Place our `download_file.py` on the payload at path `/signaling/inbox/download_file.py`, assuming the file
was successfully uploaded before the window start time.

1. Place a window configuration file at path `/signaling/window_configs/123.json`

1. Call our `payload_exec` executable using the configure flag. `nohup /usr/bin/payload_exec -u john -e -w 123 &> /dev/null &`.
Our payload_exec executable exits when it receives a configure command, so nothing will happen on the payload.

**Window start time**

At window start time the satellite bus will issue another signaling command to `payload_exec`, this time without the configure flag.  
The command executed will be `nohup /usr/bin/payload_exec -u john -w 1304893 -t 1611718292 &> /dev/null &`

`payload_exec` will do the following operations:

1. Copy `download_file.py` from the Signaling API inbox to a top level directory (`/user_exec`).
1. Load the window configuration JSON for the contact
1. Call our `download_file.py` script (now located at `/user_exec/download_file.py`) with arguments taken from the window configuration JSON.

`download_file.py` will:

1. Create a temporary file named `space.txt` with the window_id as the contents.
1. Send the file to the payloads local OORT Agent for download to the ground

**After window end**

OORT will attempt to download our `space.txt` file during the next contact opportunity.  The next contact could be up to five hours
after the end of the window.  Additionally, larger files can take multiple contacts to download.

Once the file is successfully downloaded to the ground, it will be placed in our S3 bucket and can be retrieved using:

`aws s3 cp s3://example/space.txt space.txt`