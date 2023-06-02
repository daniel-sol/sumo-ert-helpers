#!/usr/bin/env python
"""Export grid data from eclipse with metadata"""
import logging
import re
from pathlib import Path
import argparse
from fmu.dataio import ExportData
from fmu.config.utilities import yaml_load
from xtgeo import grid_from_file, gridproperty_from_file


logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)


def parse_args():
    """Parse arguments for script

    Returns:
        argparse.NameSpace: The arguments parsed
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=("Export grid data from "),
    )
    parser.add_argument("datafile", help="Path to eclipse datafile", type=str)
    parser.add_argument("config_path", help="Path to fmu config path", type=str)
    parser.add_argument("grdecl_grid", help="path to grdecl grid", type=str)
    args = parser.parse_args()
    return args


def export_egrid(datafile, exporter):
    """Export egrid file to sumo

    Args:
        datafile (str): path to datafile
    """
    egrid_path = datafile.replace(".DATA", ".EGRID")
    egrid = grid_from_file(egrid_path)
    egrid_name = re.sub(r"-\d+\.", ".", egrid.name)
    logger.info(
        "Exported to %s", exporter.export(egrid, name=egrid_name, tagname="egrid")
    )


def export_grdecl_grid(grid_path, exporter):
    """Export the grdecl grid

    Args:
        grid_path (str): path to grid

    Returns:
        xtgeo.grid: grid read from file
    """
    grid = grid_from_file(grid_path)
    print(grid.name)
    logger.info(
        "Exported to %s", exporter.export(grid, name=grid.name, tagname="grdecl_grid")
    )
    return grid


def readname(filename):
    """Read keyword from grdecl file

    Args:
        filename (str): name of file to read

    Returns:
        str: keyword name
    """
    name = ""
    linenr = 0
    with open(filename, "r", encoding="utf-8") as file_handle:
        for line in file_handle:
            linenr += 1
            print(f"{linenr}: {line}")
            if "ECHO" in line:
                continue
            match = re.match(r"^([a-zA-Z].*)", line)
            # match = re.match(r"$([a-zA-Z][0-9A-Za-z]+)\s+", line)
            if match:
                name = match.group(0)
                break
            if linenr > 20:
                break
    logger.debug("Property %s", name)

    return name


def export_grdecl_props(include_path, grid, exporter):
    """Export grid properties

    Args:
        include_path (Pathlib.Path): path where all grdecls are stored
        grid (xtgeo.Grid): grid to connect to properties
    """
    includes = include_path
    grdecls = list(includes.glob("**/*.grdecl"))
    for grdecl in grdecls:
        logger.debug(grdecl)
        name = readname(grdecl)
        if name == "":
            logger.warning("Found no name, file is probably empty")
            continue
        try:
            # Having a try after the if smacks of double dipping
            # But better safe than sorry :-)
            prop = gridproperty_from_file(grdecl, name=name, grid=grid)
            logger.info(
                "Exported to %s",
                exporter.export(prop, name=name, tagname=grid.name + "_grdecl_grid"),
            )
        except ValueError:
            logger.warning("Something wrong with reading of file")
    # print(grdecls)


def init_exporter(config_path):
    """Initialize ExportData class

    Args:
        config_path (str): path to fmu config file
    """
    exp = ExportData(config=yaml_load(config_path))
    return exp


def main():
    """Run script"""
    args = parse_args()
    exporter = init_exporter(args.config_path)
    inc_path = Path(args.datafile).parent.parent
    grid = export_grdecl_grid(args.grdecl_grid, exporter)
    export_grdecl_props(inc_path, grid, exporter)
    # export_egrid(args.datafile, exporter)


if __name__ == "__main__":
    main()
