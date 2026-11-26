#!/usr/bin/env python3
"""Make.fun entry: Make the Judge Laugh in One Line.

Writes the one-line joke to <MAKEFUN_OUTPUT_DIR>/entry.txt.
Stdlib only. Reads nothing from disk except its own ENTRY constant.
"""

import os
import sys

ENTRY = "My lawyer told me to stop saying 'allegedly' before everything. Allegedly, I am working on it."


def main() -> int:
    # Validate before writing anything.
    try:
        ENTRY.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: ENTRY is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    if not 1 <= len(ENTRY) <= 200:
        print(f"error: ENTRY length {len(ENTRY)} is outside 1-200", file=sys.stderr)
        return 1
    if not ENTRY.strip():
        print("error: ENTRY is only whitespace", file=sys.stderr)
        return 1
    for ch in ENTRY:
        if ord(ch) < 32:
            print(f"error: ENTRY contains control character U+{ord(ch):04X}", file=sys.stderr)
            return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    encoded = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(encoded)
    # Round-trip verification: read the bytes back from disk and compare
    # them to the encoded ENTRY; any mismatch (or truncation) is a failure.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != encoded:
        print(
            f"error: round-trip mismatch: wrote {len(encoded)} bytes, "
            f"read back {len(on_disk)} bytes",
            file=sys.stderr,
        )
        return 1
    if b"\n" in on_disk or b"\r" in on_disk:
        print("error: output contains a newline character", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
