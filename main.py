#!/usr/bin/env python3
"""news-image-20261121: publish the finished front page.

The page itself (entry.png, 1024x1024, 34 stories) was drawn at build
time on the build machine. This program does NOT draw anything: it only
checks the finished file and copies it to the output directory.

Standard library only — nothing is installed before this runs in the
grading container, so there are no third-party imports here at all.
Run:  python3 main.py   -> writes entry.png into /output (or the
directory named by MAKEFUN_OUTPUT_DIR).
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def die(message, code):
    print("main.py: error: " + message, file=sys.stderr)
    return code


def png_dimensions(data):
    """Return (width, height) after checking the PNG header, or None."""
    if len(data) < 33:
        return None
    if data[:8] != PNG_MAGIC:
        return None
    if data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    if not (1 <= width <= MAX_SIDE and 1 <= height <= MAX_SIDE):
        return None
    # A complete PNG ends with the 12-byte IEND chunk; a truncated
    # file must not pass validation even if its header looks fine.
    if data[-12:] != struct.pack(">I4sI", 0, b"IEND", 0xAE426082):
        return None
    return width, height


def output_dir():
    """Where the graded image goes: env override, /output, else local."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        return wanted
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(HERE, "output")


def main():
    if not os.path.isfile(SRC):
        return die("entry.png not found next to main.py", 2)
    with open(SRC, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        return die("entry.png is %d bytes, over the %d limit"
                   % (len(data), MAX_BYTES), 2)
    dims = png_dimensions(data)
    if dims is None:
        return die("entry.png is not a valid PNG of at most "
                   "%dx%d" % (MAX_SIDE, MAX_SIDE), 2)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(data)
    with open(out_path, "rb") as handle:
        written = handle.read()
    if written != data:
        return die("output did not match entry.png after copy", 3)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s %d bytes %dx%d sha256=%s"
          % (out_path, len(data), dims[0], dims[1], digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
