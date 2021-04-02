#!/usr/bin/python3
import argparse
import json
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-e', dest='configure', default=False, type=bool, help='Configure flag')
parser.add_argument('-w', dest='window_id', default=None, type=int, help='ID of window')
parser.add_argument('-t', dest='end_time', default=None, type=str, help='End of the window (unix timestamp)')
parser.add_argument('-u', dest='user', default=None, type=str, help='Tasking API user')

EXECUTABLE_DIRECTORY = '/user_exec'

if __name__ == "__main__":
    args = parser.parse_args()
    if args.configure:
        # A configure signal was received.
        # This is not implemented for this example, so exit with a successful status code
        exit(0)

    # Check to see if our executable is located in our inbox
    uplinked_files = os.listdir(f'/signaling/inbox/{args.user}')

    for file_name in uplinked_files:
        os.rename(f'/signaling/inbox/{args.user}/{file_name}', f'{EXECUTABLE_DIRECTORY}/{file_name}')

    # Parse window configuration
    with open(f'/signaling/window_configs/{args.window_id}.json', 'rb') as f:
        config = json.load(f)
        executable_name = config['signal_parameters']['tasking_parameters']['executable']
        file_name = config['signal_parameters']['tasking_parameters']['filename']

        # Call our executable
        os.system(f'{EXECUTABLE_DIRECTORY}/{executable_name} -w {args.window_id} -n {file_name}')
