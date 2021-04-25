import subprocess as subp
import os
from .util import write_and_flush


class ErrorWriter:
    def __init__(self):
        self.lines = []

    def __call__(self, line):
        self.lines.append(line)

    def show(self):
        text = "".join(self.lines)
        if len(self.lines) > os.get_terminal_size().lines:
            pager = os.environ.get("PAPER", "less")
            subp.run([pager, "-"], input=text.encode())
        else:
            write_and_flush(text)
