#!/usr/bin/python3

import argparse

from oort_sdk_client import SdkApi
from oort_sdk_client.models import (
    SendFileRequest, SendOptions, TTLParams
)

parser = argparse.ArgumentParser(description='Create and download a file from our payload to the ground.')
parser.add_argument('-n', dest='filename', type=str, help='Filename to create and download.')
parser.add_argument('-w', dest='window_id', type=str, help='ID of window.')

OORT_TOPIC = 'example'

if __name__ == '__main__':
    args = parser.parse_args()
    file_path = f'/tmp/{args.file_name}'

    with open(file_path, 'wb') as f:
        f.write(args.window_id)

    # Initialize our OORT Agent
    agent = SdkApi()

    # Send our file to OORT
    req = SendFileRequest(
        destination="ground",
        topic=OORT_TOPIC,
        filepath=file_path,
        options=SendOptions())
    resp = agent.send_file(req)
