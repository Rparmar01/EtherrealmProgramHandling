"""
Python 3 code that can decompress (to a .gvas file), or recompress (to a .savegame file)
the UE4 savegame file that Astroneer uses.
Though I wrote this for tinkering with Astroneer games saves, it's probably
generic to the Unreal Engine 4 compressed saved game format.
Examples:
ue4_save_game_extractor_recompressor.py --extract  --file z2.savegame  # Creates z2.gvas
ue4_save_game_extractor_recompressor.py --compress --file z2.gvas      # Creates z2.NEW.savegame
ue4_save_game_extractor_recompressor.py --test     --file z2.savegame  # Creates *.test files
---
Copyright (c) 2016-2020 Martin Falatic
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import os
import sys
import zlib

HEADER_FIXED_HEX = "BE 40 37 4A EE 0B 74 A3 01 00 00 00"
HEADER_FIXED_BYTES = bytes.fromhex(HEADER_FIXED_HEX)
HEADER_FIXED_LEN = len(HEADER_FIXED_BYTES)
HEADER_RAW_SIZE_LEN = 4
HEADER_GVAS_MAGIC = b'GVAS'
COMPRESSED_EXT = 'savegame'
EXTRACTED_EXT = 'gvas'


def extract_data(filename_in, filename_gvas):
    data_gvas = bytes()
    with open(filename_in, 'rb') as compressed:
        header_fixed = compressed.read(HEADER_FIXED_LEN)
        header_raw_size = compressed.read(HEADER_RAW_SIZE_LEN)
        gvas_size = int.from_bytes(header_raw_size, byteorder='little')
        header_hex = ''.join('{:02X} '.format(x) for x in header_fixed)
        if HEADER_FIXED_BYTES != header_fixed:
            print(f"Header bytes do not match: Expected '{HEADER_FIXED_HEX}' got '{header_hex}'")
            sys.exit(1)
        data_compressed = compressed.read()
        data_gvas = zlib.decompress(data_compressed)
        sz_in = len(data_compressed)
        sz_out = len(data_gvas)
        if gvas_size != sz_out:
            print(f"gvas size does not match: Expected {gvas_size} got {sz_out}")
            sys.exit(1)
        with open(filename_gvas, 'wb') as gvas:
            gvas.write(data_gvas)
        header_magic = data_gvas[0:4]
        if HEADER_GVAS_MAGIC != header_magic:
            print(f"Warning: Raw save data magic: Expected {HEADER_GVAS_MAGIC} got {header_magic}")
        print(f"Inflated from {sz_in:d} (0x{sz_in:0x}) to {sz_out:d} (0x{sz_out:0x}) bytes as {filename_gvas}")
    return data_gvas


def compress_data(filename_gvas, filename_out):
    data_gvas = None
    data_compressed = bytes()
    with open(filename_gvas, 'rb') as gvas:
        data_gvas = gvas.read()
    header_magic = data_gvas[0:4]
    if HEADER_GVAS_MAGIC != header_magic:
        print(f"Warning: Raw save data magic: Expected {HEADER_GVAS_MAGIC} got {header_magic}")
    with open(filename_out, 'wb') as compressed:
        compress = zlib.compressobj(
            level=zlib.Z_DEFAULT_COMPRESSION,
            method=zlib.DEFLATED,
            wbits=4+8,  # zlib.MAX_WBITS,
            memLevel=zlib.DEF_MEM_LEVEL,
            strategy=zlib.Z_DEFAULT_STRATEGY,
        )
        data_compressed += compress.compress(data_gvas)
        data_compressed += compress.flush()
        compressed.write(HEADER_FIXED_BYTES)
        compressed.write(len(data_gvas).to_bytes(HEADER_RAW_SIZE_LEN, byteorder='little'))
        compressed.write(data_compressed)
        sz_in = len(data_gvas)
        sz_out = len(data_compressed)
        print(f"Deflated from {sz_in:d} (0x{sz_in:0x}) to {sz_out:d} (0x{sz_out:0x}) bytes as {filename_out}")
    return data_compressed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UE4 Savegame Extractor/Compressor")
    parser.add_argument('--filename')
    parser.add_argument('--extract', action='store_true')
    parser.add_argument('--compress', action='store_true')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    argerrors = False
    if not args.filename:
        print("Error: No filename specified")
        argerrors = True
    if (args.extract and args.compress):
        print("Error: Choose only one of --extract or --compress")
        argerrors = True
    if (args.extract or args.compress) and args.test:
        print("Error: --test switch stands alone")
        argerrors = True
    if argerrors:
        sys.exit(1)

    filename = args.filename
    dirname, basename = os.path.split(filename)
    rootname, extname = os.path.splitext(basename)

    if args.extract:
        filename_in = filename
        filename_gvas = os.path.join(dirname, f'{rootname}.{EXTRACTED_EXT}')
        data_gvas = extract_data(filename_in=filename_in, filename_gvas=filename_gvas)
    elif args.compress:
        filename_gvas = filename
        filename_out = os.path.join(dirname, f'{rootname}.NEW.{COMPRESSED_EXT}')
        data_compressed = compress_data(filename_gvas=filename, filename_out=filename_out)
    elif args.test:
        filename_in = filename
        filename_gvas_1 = os.path.join(dirname, f'{rootname}.{EXTRACTED_EXT}.1.test')
        filename_out = os.path.join(dirname, f'{rootname}.NEW.{COMPRESSED_EXT}.test')
        filename_gvas_2 = os.path.join(dirname, f'{rootname}.{EXTRACTED_EXT}.2.test')
        data_gvas = extract_data(filename_in=filename_in, filename_gvas=filename_gvas_1)
        data_compressed = compress_data(filename_gvas=filename_gvas_1, filename_out=filename_out)
        data_check = extract_data(filename_in=filename_out, filename_gvas=filename_gvas_2)
        status = "Passed" if data_gvas == data_check else "Failed"
        print()
        print(f"{status}: Tested decompress-compress-decompress")