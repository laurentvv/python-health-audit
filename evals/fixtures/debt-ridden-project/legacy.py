"""Legacy module kept 'just in case' (planted dead code for Vulture)."""

import hashlib
import shutil


class OldReportBuilder:
    """Dead class: nothing imports or instantiates it anymore."""

    def __init__(self, title="report"):
        self.title = title
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def render(self):
        return self.title + "\n" + "\n".join(self.rows)


def old_helper(payload, salt="x"):
    """Dead function: superseded by services.csv_import, never called."""
    digest = hashlib.sha256((salt + payload).encode()).hexdigest()
    return digest[:16]


def another_dead_function(path):
    """Dead function: leftover from the pre-refactor era."""
    shutil.rmtree(path, ignore_errors=True)
    return True


old_mode = "compat"  # dead variable: read by no one
