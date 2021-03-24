#!/bin/bash

HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SATELLITE_ID="FM200"
DURATION="60"
PAYLOAD="MY_PAYLOAD_NAME"
EXECUTABLE="true"
DESTINATION_PATH="download_file.py"
CURR_TIME=$(`date -u +%s`)

# Note that this is 24hrs in the future to allow enough time for file upload.
# Estimated upload time will vary depending on uplink size.
# For large files, it is recommended to wait until the upload completes to schedule a window
START_TIME=$((${CURR_TIME}+60*60*24))

# Upload our binary
QUERY_PARAMS="satellite=${SATELLITE_ID}&payload=${PAYLOAD}&destination_path=${DESTINATION_PATH}&executable=${EXECUTABLE}"

# Upload our python script
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@download_file.py"

# Create the Tasking Window
curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_${PAYLOAD_NAME}",
    "satellite_id": "${SATELLITE_ID}",
    "start": ${START_TIME},
    "duration": 600,
    "parameters": {
        "executable": "download_file.py",
        "filename": "foo.txt"
    }
}
EOF
