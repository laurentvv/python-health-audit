"""Excluded decoy: a fake dependency inside .venv.

Every audit step must skip this file. It contains a third copy of the
planted parse_csv_line block, so a regression in Pylint's --ignore handling
of dot-directories (seen on Windows with --ignore-paths) would surface as
an R0801 pair mentioning this file.
"""


def parse_csv_line_decoy(line):
    """Third copy of the duplicated block — must stay invisible."""
    fields = []
    current = []
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == "," and not in_quotes:
            fields.append("".join(current))
            current = []
        else:
            current.append(char)
    fields.append("".join(current))
    return fields
