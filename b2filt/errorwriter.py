import subprocess as subp
import os
import shlex
from .util import write_and_flush


class ErrorWriter:
    def __init__(self):
        self.lines = []

    def __call__(self, line):
        self.lines.append(line)

    def show(self):
        text = "".join(self.lines)
        try:  # os.get_terminal_size() can fail, e.g. when this is called by pytest
            max_lines = os.get_terminal_size().lines
        except OSError:
            max_lines = 50
        if len(self.lines) < max_lines:
            write_and_flush(text)
        else:
            pager = os.environ.get("PAGER", "less -r")
            p = subp.run(shlex.split(pager) + ["-"], input=text.encode())
            if p.returncode != 0:
                write_and_flush(f"Error in PAGER {pager}, printing output...\n")
                write_and_flush(text)
