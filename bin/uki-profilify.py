#!/usr/bin/env python3
# uki-profilify.py: uki-profilify script
#
# Copyright 2024 Fleuria
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import tomllib

# helpers

# UKI writers

if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='uki-in')
    parser.add_argument('-c', '--config', metavar='config',
                        help='configuration file')
    parser.add_argument('-o', '--output', metavar='uki-out',
                        help='UKI output filename')
    # # parse options
    args = parser.parse_args()

    # handle inputs
    # # error handling: is uki-in actually a file?
    if not os.path.isfile(args.input):
        raise FileNotFoundError("'{}' does not exist".format(args.input))
    # # and is it an EFI executable?
    (name, ext) = os.path.splitext(os.path.basename(args.input))
    if ext != '.efi':
        raise TypeError("'{}' is not an EFI executable".format(args.input))

    # get config
    # # select the config file path
    config_file = args.config \
        if args.config \
        else "/etc/uki-profilify/{}.toml".format(name)
    # # then load it
    config = None
    with open(config_file, 'rb') as f:
        config = tomllib.load(f)
    # # add 'options' if nonexistent, to avoid erroring in next steps
    config = {'options': {}} | config
    # # handle the --output option
    if args.output:
        config['options']['output'] = args.output
    # # sanity check: does the output directory actually exist?
    if 'output' in config['options']:
        outdir = os.path.dirname(config['options']['output'])
        if not os.path.isdir(outdir):
            raise FileNotFoundError("{} is not a valid directory"
                                    .format(outdir))

    # generate profiles
    pass

    # pack UKI
    pass
