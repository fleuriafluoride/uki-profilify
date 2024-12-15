#!/usr/bin/env python3
# uki-profilify.py: uki-profilify script
#
# Copyright 2024 Fleuria
# SPDX-License-Identifier: Apache-2.0

import argparse
import itertools
import os
import subprocess
import tempfile
import tomllib

_config_dir = '/etc/uki-profilify'

# helpers


def check_if_file(apath):
    if apath is None:
        return  # do nothing
    if not os.path.isfile(apath):
        raise FileNotFoundError("No such file: {}".format(apath))


def check_if_dir_viable(outpath):
    dir = os.path.dirname(outpath)
    if not os.path.isdir(dir):
        raise FileNotFoundError("No such directory: {}".format(dir))


def set_if_not_none(dict, key, newval):
    if newval is not None:
        dict[key] = newval


def default_if_none(var, default):
    return var if var is not None else default


# extracted code segments


def _set_args(parser):
    parser.add_argument('kernel')
    parser.add_argument('initramfs', nargs='?')
    parser.add_argument('-a', '--auto', action='store_true',
                        help='set automatic mode')
    parser.add_argument('-c', '--config', metavar='conf',
                        help='configuration file')
    parser.add_argument('-o', '--output', metavar='filepath',
                        help='UKI output filename')


def _find_config(kernel):
    confs = [name
             for entry in os.scandir(_config_dir)
             if entry.is_file()
             for name, ext in [os.path.splitext(entry.name)]
             if ext == '.toml']
    confs.sort(key=len, reverse=True)
    for c in confs:
        if c in kernel:
            return _config_dir + "/{}.toml".format(c)
    # no configuration exists; exit now
    print("No configuration file found for {}, exiting".format(kernel))
    sys.exit()


def _enforce_auto_flag(args, uki):
    if args.auto:
        if uki['initrd'] != aargs.initramfs:
            print('initramfs does not match in auto mode, exiting')
            sys.exit()


def build_profile(profile, number, dir):
    print(profile)
    print(number)
    print(dir)


def build_multiprofile_uki(kernel, conf_uki, profiles):
    print(kernel)
    print(conf_uki)
    print(profiles)


# the main code

if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser()
    _set_args(parser)
    args = parser.parse_args()

    # input sanitisation: is kernel a real file?
    check_if_file(args.kernel)

    # get config and load
    config_file = default_if_none(args.config, _find_config(args.kernel))
    with open(config_file, 'rb') as f:
        config = tomllib.load(f)

    # get uki table; default to empty table if not found
    conf_uki = config.get('uki', {})

    # apply options
    _enforce_auto_flag(args, conf_uki)
    set_if_not_none(conf_uki, 'output', args.output)
    set_if_not_none(conf_uki, 'initrd', args.initramfs)
    check_if_dir_viable(conf_uki['output'])
    check_if_file(conf_uki['initrd'])

    # generate some UKIs!
    with tempfile.TemporaryDirectory() as tmpd:
        # first, profiles
        counter = itertools.count()
        profile_files = [build_profile(profile, number, tmpd)
                         for profile in config['profiles']
                         for number in [next(counter)]]

        # then, the complete UKI
        build_multiprofile_uki(args.kernel, conf_uki, profile_files)
