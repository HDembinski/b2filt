#!/usr/bin/python3
import subprocess as subp
import sys
from pathlib import Path
import time
import os

write = sys.stdout.write
flush = sys.stdout.flush


class ErrorWriter:
    def __init__(self):
        self.lines = []

    def __call__(self, line):
        self.lines.append(line)

    def show(self):
        pager = os.environ.get("PAPER", "less")
        subp.run([pager, "-"], input="".join(self.lines).encode())


error = ErrorWriter()

reset = "\x1b[0m"
black = "\x1b[30m"
red = "\x1b[31m"
green = "\x1b[32m"
yellow = "\x1b[33m"
blue = "\x1b[34m"
magenta = "\x1b[35m"
cyan = "\x1b[36m"
white = "\x1b[37m"


def short_label(label):
    if "compile" in label:
        return f"{magenta}C{reset}"
    elif "link" in label:
        return f"{yellow}L{reset}"
    elif "passed" in label:
        return f"{green}✓{reset}"
    elif "testing" in label or "capture" in label:
        return f"{blue}T{reset}"
    elif "archive" in label:
        return None
    raise ValueError(label)


def clear_line(nmax):
    write("\r" + " " * (nmax))  # clear line
    flush()


def find_b2():
    wd = Path()
    while wd.exists():
        p = wd / "b2"
        if p.exists():
            return f"./{p}"
        wd = wd / ".."
    return "b2"


def main():
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
    found_compile_error = False
    try:
        for line in p.stdout:
            if line == "====== BEGIN OUTPUT ======\n":
                nerror += 1
                continue
            if (
                line.startswith("In file included from")
                or "In instantiation of" in line
            ):
                nerror += 1
                found_compile_error = True
            if line == "====== END OUTPUT ======\n":
                skip = True
            if line.startswith("..."):
                continue
            if line.startswith("link.mklink"):
                continue
            try:
                label, path = line.split()
                path = Path(path)
                if not path.exists():
                    raise ValueError  # make it a non-match
                slabel = short_label(label)
                skip = False
                first_error_line = True
                if slabel is None:
                    continue
                s = f"\r{slabel} {path.stem}"
                if nmax == 0:
                    write("\n")
                nmax = max(len(s), nmax)
                clear_line(nmax)
                write(s)
            except ValueError:
                if first_error_line:
                    write("\n")
                    first_error_line = False
                if not skip:
                    if found_compile_error:
                        error(line)
                    else:
                        write(line)
            flush()
        if nerror == 0 and nmax:
            clear_line(nmax)
            dt = time.monotonic() - t_start
            write(f"\r{int(dt / 60):02}:{int(dt % 60):02}\n")
    except KeyboardInterrupt:
        p.kill()
        sys.exit(2)
    if found_compile_error:
        error.show()
    if nerror:
        sys.exit(1)
