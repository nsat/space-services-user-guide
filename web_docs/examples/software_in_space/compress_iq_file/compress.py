#!/usr/bin/python3
import argparse
import lzma

parser = argparse.ArgumentParser(
    description='Compress a file using xz from an input path and save to output path.'
)
parser.add_argument('--input', help='Path of file to compress.')
parser.add_argument('--output', help='Path to save compressed file to.')

if __name__ == '__main__':
    args = parser.parse_args()

    # Create file objects for our input and output files
    with open(args.input, 'rb') as original, open(args.output, 'wb') as compressed:
        # Compress our input file and save to output path
        compressed.write(lzma.compress(bytes(original.read())))
