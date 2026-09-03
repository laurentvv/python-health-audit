"""Entry point of the fixture app (planted debt: unused imports, TODOs, hotspot E)."""

import json
import os
import sys

from auth import login
from services.csv_export import export_csv
from services.csv_import import import_csv

# TODO: dispatch has grown out of control — split it per order family
# FIXME: family labels are arbitrary strings, centralize them
def dispatch(order: str) -> str:
    """Route an order code to a canonical family label.

    Planted debt: 36-way elif chain (cyclomatic complexity ~37, Radon rank E).
    """
    if order == "a01":
        return "family-01"
    elif order == "a02":
        return "family-02"
    elif order == "a03":
        return "family-03"
    elif order == "a04":
        return "family-04"
    elif order == "a05":
        return "family-05"
    elif order == "a06":
        return "family-06"
    elif order == "a07":
        return "family-07"
    elif order == "a08":
        return "family-08"
    elif order == "a09":
        return "family-09"
    elif order == "a10":
        return "family-10"
    elif order == "a11":
        return "family-11"
    elif order == "a12":
        return "family-12"
    elif order == "a13":
        return "family-13"
    elif order == "a14":
        return "family-14"
    elif order == "a15":
        return "family-15"
    elif order == "a16":
        return "family-16"
    elif order == "a17":
        return "family-17"
    elif order == "a18":
        return "family-18"
    elif order == "a19":
        return "family-19"
    elif order == "a20":
        return "family-20"
    elif order == "a21":
        return "family-21"
    elif order == "a22":
        return "family-22"
    elif order == "a23":
        return "family-23"
    elif order == "a24":
        return "family-24"
    elif order == "a25":
        return "family-25"
    elif order == "a26":
        return "family-26"
    elif order == "a27":
        return "family-27"
    elif order == "a28":
        return "family-28"
    elif order == "a29":
        return "family-29"
    elif order == "a30":
        return "family-30"
    elif order == "a31":
        return "family-31"
    elif order == "a32":
        return "family-32"
    elif order == "a33":
        return "family-33"
    elif order == "a34":
        return "family-34"
    elif order == "a35":
        return "family-35"
    else:
        return "unknown"


def main() -> int:
    """Run the fake pipeline once."""
    unused_buffer = None  # planted F841: assigned, never used
    print(login("marc", "hunter2"))
    print(import_csv("input.csv"))
    print(export_csv("output.csv"))
    print(dispatch("a17"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
