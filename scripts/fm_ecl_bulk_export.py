#!/usr/bin/env python
import os
import logging
import argparse
from ecl2df.bulk import bulk_export_with_configfile

logging.basicConfig(level="DEBUG")


def parse_args():
    """Parse arguments for script

    Returns:
        argparse.NameSpace: The arguments parsed
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=("Export all available datatypes from eclipse run"),
    )
    parser.add_argument("runpath", help="path to folder to run in", type=str)
    parser.add_argument("eclpath", help="Path to eclipse datafile", type=str)
    parser.add_argument("fmu_config_path", help="Path to fmu config path", type=str)
    args = parser.parse_args()
    return args


def export(args):
    """Export all datatypes from eclipse present

    Args:
        args (argparse.NameSpace): the arguments parsed by script
    """
    os.chdir(args.runpath)
    bulk_export_with_configfile(args.fmu_config_path, args.eclpath)


def main():
    """Run script"""
    args = parse_args()
    export(args)


if __name__ == "__main__":
    main()
