import sys
from pathlib import Path


def colored_text(txt, color):
    esc = "\x1b[{}m"
    reset = esc.format(0)
    code = esc.format(
        {
            "k": 30,
            "r": 31,
            "g": 32,
            "y": 33,
            "b": 34,
            "m": 35,
            "c": 36,
            "w": 37,
        }[color]
    )
    return f"{code}{txt}{reset}"


def write_and_flush(x):
    sys.stdout.write(x)
    sys.stdout.flush()


def is_compile(x):
    return "compile" in x


def short_label(label):
    if is_compile(label):
        return colored_text("C", "m")
    elif "link" in label:
        return colored_text("L", "y")
    elif "passed" in label:
        return colored_text("✓", "g")
    elif "testing" in label or "capture" in label:
        return colored_text("T", "b")
    elif "archive" in label:
        return None
    raise ValueError(label)


def clear_line(nmax):
    write_and_flush("\r" + " " * (nmax) + "\r")  # clear line


def find_b2():
    wd = Path().absolute()
    while wd.parent != wd:
        p = wd / "b2"
        if p.exists():
            return p
        wd = wd.parent
    return "b2"
