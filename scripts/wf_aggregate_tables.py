#!/usr/bin/env python
"""Author dbs: aggregates summary files, splits up by vector"""
import argparse
import logging
from pathlib import Path
from fmu.config.utilities import yaml_load
from sumo.table_aggregation import AggregationRunner

# from sumo-table-service import caller
logging.basicConfig(level="INFO")
LOGGER = logging.getLogger(__name__)


def find_uuid(case_meta_path):
    """Find case uuid from file

    Args:
        case_meta_path (str): path to file
    """
    meta = yaml_load(Path(case_meta_path) / "share/metadata/fmu_case.yml")
    return meta["fmu"]["case"]["uuid"]


def parse_args():
    """Parses the arguments required
    returns:
    args: arguments as name space
    """
    form_class = argparse.ArgumentDefaultsHelpFormatter
    description = "Splits table data uploaded to sumo into 'single objects' per column "
    parser = argparse.ArgumentParser(
        formatter_class=form_class, description=description
    )
    parser.add_argument("scratch_path", type=str, help="path to scratch ensemble")

    parser.add_argument(
        "-env", help="What sumo environment to upload to", type=str, default="prod"
    )

    parser.add_argument("-d", help="debug mode", action="store_true")

    args = parser.parse_args()

    LOGGER.debug(args)
    return args


def aggregate_tables(uuid, env):
    """Aggregate all tables in case"""

    aggregator = AggregationRunner(uuid, env)
    aggregator.run()


def main():
    """Extracts the vectors, splits"""

    args = parse_args()
    uuid = find_uuid(args.scratch_path)
    LOGGER.debug("Uuid of case %s", uuid)
    aggregate_tables(uuid, args.env)
    LOGGER.info("All done splitting!")


if __name__ == "__main__":
    main()
