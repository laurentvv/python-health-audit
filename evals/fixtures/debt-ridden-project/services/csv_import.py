"""CSV import service (contains copy #1 of the planted duplicated block)."""


def parse_csv_line(line):
    """Parse one CSV line into fields, honouring double quotes.

    Planted debt: body duplicated verbatim in services/csv_export.py.
    """
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


def import_csv(path: str) -> list:
    """Read the file (here: simulate) and parse each line."""
    rows = []
    for line in ["alpha,beta", '"gamma,1",2']:
        rows.append(parse_csv_line(line))
    return rows + [path]
