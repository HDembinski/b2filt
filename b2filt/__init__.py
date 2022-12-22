"""
b2filt is a filter for b2 output.

See README.md on GitHub for details.
"""

__version__ = "0.2.2"

from .errorwriter import ErrorWriter
from .util import (
    find_b2,
    clear_line,
    short_label,
    write_and_flush,
    is_compile,
    colored_text,
)
import time
import subprocess as subp
import sys
from pathlib import Path


def main():
    """Run b2 and parse its output."""
    error = ErrorWriter()

    t_start = time.monotonic()
    p = subp.Popen(
        [find_b2()] + sys.argv[1:],
        stdout=subp.PIPE,
        stderr=subp.STDOUT,
        text=True,
        bufsize=1,
    )
    nmax = 0
    skip = False
    first_error_line = True
    nerror = 0
    previous_line = ""
    compile_error = False
    try:
        for line in p.stdout:
            if line == "====== BEGIN OUTPUT ======\n":
                nerror += 1
                continue
            if line == "====== END OUTPUT ======\n":
                skip = True
            if line.startswith("...failed") and "compile" in line:
                nerror += 1
                compile_error = False
                continue
            if line.startswith("(failed-as-expected)"):
                compile_error = False
                error(line)
                continue
            if line.startswith("..."):
                continue
            if line.startswith("link.mklink"):
                continue
            try:
                label, path, *rest = line.split()
                if len(rest) > 0:
                    raise ValueError
                slabel = short_label(label)
                skip = False
                first_error_line = True
                if slabel is None:
                    continue
                s = f"\r{slabel} {Path(path).stem}"
                if nmax == 0:
                    write_and_flush("\n")
                nmax = max(len(s), nmax)
                clear_line(nmax)
                write_and_flush(s)
            except ValueError:
                if not skip:
                    if is_compile(previous_line):
                        compile_error = True
                        label, path = previous_line.split()
                        error(f"{colored_text('Compile error', 'm')} {path}\n")
                    if compile_error:
                        error(line)
                    else:
                        if first_error_line:
                            first_error_line = False
                            write_and_flush("\n")
                        write_and_flush(line)
            previous_line = line

        clear_line(nmax)
        if nerror == 0 and nmax:
            dt = time.monotonic() - t_start
            write_and_flush(f"\r{int(dt / 60):02}:{int(dt % 60):02}\n")
        error.show()

    except KeyboardInterrupt:
        p.kill()
        sys.exit(2)
    if nerror:
        sys.exit(1)
