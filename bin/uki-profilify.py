#!/usr/bin/env python3
# uki-profilify.py: uki-profilify script
#
# Copyright 2024 Fleuria
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
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


def _set_args(aparser):
    aparser.add_argument('kernel')
    aparser.add_argument('initramfs', nargs='?')
    aparser.add_argument('-a', '--auto', action='store_true',
                         help='set automatic mode')
    aparser.add_argument('-c', '--config', metavar='conf',
                         help='configuration file')
    aparser.add_argument('-o', '--output', metavar='filepath',
                         help='UKI output filename')


def _find_config(akernel):
    confs = [name
             for entry in os.scandir(_config_dir)
             if entry.is_file()
             for (name, ext) in [os.path.splitext(entry.name)]
             if ext == '.toml']
    confs.sort(key=len, reverse=True)
    for c in confs:
        if c in akernel:
            return _config_dir + "/{}.toml".format(c)
    # no configuration exists; exit now
    print("No configuration file found for {}, exiting".format(akernel))
    sys.exit()


def _enforce_auto_flag(aargs, auki):
    if aargs.auto:
        if auki['initrd'] != aargs.initramfs:
            print('initramfs does not match in auto mode, exiting')
            sys.exit()


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

    # generate profiles
    pass

    # create UKI
    pass
