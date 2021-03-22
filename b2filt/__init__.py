#!/usr/bin/python3
import subprocess as subp
import sys
from pathlib import PurePath, Path
import time

write = sys.stdout.write
flush = sys.stdout.flush

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
    raise ValueError(label)


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
    try:
        for line in p.stdout:
            if line == "====== BEGIN OUTPUT ======\n":
                continue
            if line == "====== END OUTPUT ======\n":
                skip = True
            if line.startswith("..."):
                skip = False
                continue
            if line.startswith("link.mklink"):
                skip = False
                continue
            try:
                label, path = line.split()
                if "archive" in label:
                    skip = False
                    continue
                path = PurePath(PurePath(path).stem)
                short = path.parts[-1]
                s = short_label(label)
                skip = False
                first_error_line = True
                s = f"\r{s} {short}"
                if nmax == 0:
                    write("\n")
                nmax = max(len(s), nmax)
                write("\r" + " " * (nmax))  # clear line
                flush()
                write(s)
            except ValueError:
                if first_error_line:
                    write("\n")
                    first_error_line = False
                if not skip:
                    write(line)
            flush()
        dt = time.monotonic() - t_start
        if nmax:
            write("\r" + " " * (nmax))  # clear line
            flush()
            write(f"\r{int(dt / 60):02}:{int(dt % 60):02}\n")
    except KeyboardInterrupt:
        p.kill()
        raise SystemExit
