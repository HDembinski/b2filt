#!/usr/bin/python3
import subprocess as subp
import sys
from pathlib import Path
import time
import os


def write_and_flush(x):
    sys.stdout.write(x)
    sys.stdout.flush()


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


def is_compile(x):
    return "compile" in x


def short_label(label):
    if is_compile(label):
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
    write_and_flush("\r" + " " * (nmax) + "\r")  # clear line


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
                compile_error = False
                continue
            if line.startswith("..."):
                continue
            if line.startswith("link.mklink"):
                continue
            try:
                label, path = line.split()
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
                        error(f"{magenta}Compile error{reset} {path}\n")
                        nerror += 1
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
