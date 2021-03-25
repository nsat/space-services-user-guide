#!/bin/bash

HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SATELLITE_ID="FM200"
DURATION="60"
PAYLOAD="SDR"
EXECUTABLE="true"
DESTINATION_PATH="/usr/bin/sdr_processor"
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
-F "file=@sdr_processor.py"

# Create the Tasking Window
# This window will execute an SDR capture and process the generated IQ file using our sdr_processor script
curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SDR",
    "satellite_id": "${SATELLITE_ID}",
    "start": ${START_TIME},
    "duration": 600,
    "parameters": {
        "downlink_budget": 0,
        "capture_config": {
            "capture_duration": 60,
            "frequency_band": "VHF",
            "adc_config": {
              "bandwidth_khz": 4000,
              "sample_rate_khz": 12500,
              "frequency_khz": 1090,
              "buffer": 4000,
              "gain_ctrl": "slow_attack",
              "gain": 0,
              "fir_config": "/persist/config/fir.txt"
            },
            "adcs_config": {
              "mode": "TRACKING",
              "target_latitude_north": 25.5,
              "target_longitude_east": -71.5
            }
        },
        "user_command": {
          "executable": "/usr/bin/sdr_processor",
          "executable_arguments": [
              "--input", "/inbox/capture.iq",
              "--output", "/outbox/output.txt"
          ]
        }
    }
}
EOF
