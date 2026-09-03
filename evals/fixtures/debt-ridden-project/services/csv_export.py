"""CSV export service (contains copy #2 of the planted duplicated block)."""


def parse_csv_line(line):
    """Parse one CSV line into fields, honouring double quotes.

    Planted debt: body duplicated verbatim from services/csv_import.py.
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


def export_csv(path: str) -> str:
    """Serialize a couple of demo rows through the shared parser."""
    lines = []
    for row in [["alpha", "beta"], ['"gamma,1"', "2"]]:
        lines.append(",".join(row))
    parsed = [parse_csv_line(line) for line in lines]
    return path + ":" + str(len(parsed))
