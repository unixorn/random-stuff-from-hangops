#!/usr/bin/env python3
#
# By @ascentdantlogic on hangops slack
#
# MIT Licensed

from typing import List
from rich.console import Console
from rich.table import Table
import boto3
import sys

def _get_parameters(group: str) -> dict[str, str]:
    params = {}
    token = None

    while(True):
        if token == False:
            break
        elif token == None:
            chunk = rds.describe_db_parameters(DBParameterGroupName=group)
        else:
            chunk = rds.describe_db_parameters(DBParameterGroupName=group, Marker=token)

        for param in chunk["Parameters"]:
            params[param["ParameterName"]] = param.get("ParameterValue", "")

        token = chunk.get("Marker", False)

    return params


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"USAGE: {sys.argv[0]} GROUP1 GROUP2")
        exit(1)
        
    keys = set()

    group1 = sys.argv[1]
    group2 = sys.argv[2]

    rds = boto3.client("rds")

    first = _get_parameters(group1)
    second = _get_parameters(group2)

    # create a sorted union set of the parameters
    keys = sorted(first.keys() | second.keys())

    console = Console()
    table = Table(show_header=True, header_style="bold white")
    table.add_column("Parameter")
    table.add_column(group1)
    table.add_column(group2)

    for key in keys:
        first_value = first.get(key, "")
        second_value = second.get(key, "")

        if first_value == "" and second_value == "":
            continue

        if first_value != second_value:
            table.add_row(key, first_value, second_value, style="bold yellow")
        else:
			# uncomment if you want to see params that have identical values between groups
			# table.add_row(key, first_value, second_value, style="bold green")
            continue

    console.print(table)
