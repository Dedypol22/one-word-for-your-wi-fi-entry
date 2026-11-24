"""One Word for Your Wi-Fi.

Entry for the make.fun bounty "One Word for Your Wi-Fi"
(u-tuan-muda-one-word-for-your-wi-fi-a1b4fd72).

The deliverable is a single word describing Wi-Fi. The word is "Liar":
the Wi-Fi lies -- full signal bars, "Connected, no internet", and
nothing loads. The joke is an accusation, not a description of speed:
the network claims to be connected while delivering nothing, and
anyone who has stared at full bars while a page refuses to load
recognises it instantly. One word, no setup needed, no explanation
required -- that is what the judge rewards.

When run, this program writes the word to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when that
variable is not set), self-checking the entry rules first.
"""

import os
import sys

# The entry: an accusation aimed at the router. Full bars, no internet.
WORD = "Liar"

# The bounty caps the entry at 20 characters, but the winning word
# does not need the room: "Liar" is four characters and lands the
# joke in one punch. Full bars, "Connected, no internet", nothing
# loads -- the network claims to be connected while delivering
# nothing, so the word is an accusation, not a description of speed.
# Funny at once, instantly recognisable to anyone who has stared at
# full bars while a page refuses to load. The limit is enforced as
# a hard rule, not a target length to fill.
MAX_LENGTH = 20


def main() -> int:
    # Self-check the deliverable before writing it.
    if not WORD:
        print("error: the entry word is empty", file=sys.stderr)
        return 1
    if any(ch.isspace() for ch in WORD):
        print(
            f"error: the entry word {WORD!r} contains whitespace "
            "(must be exactly one word)",
            file=sys.stderr,
        )
        return 1
    if len(WORD) > MAX_LENGTH:
        print(
            f"error: the entry word is {len(WORD)} characters, "
            f"over the {MAX_LENGTH}-character limit",
            file=sys.stderr,
        )
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output_path = os.path.join(output_dir, "entry.txt")

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(WORD)
    except OSError as exc:
        print(f"error: could not write {output_path}: {exc}", file=sys.stderr)
        return 1

    # Read the file back and verify it matches exactly.
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            written = f.read()
    except OSError as exc:
        print(f"error: could not read back {output_path}: {exc}", file=sys.stderr)
        return 1

    if written != WORD:
        print(
            f"error: entry.txt does not match the word "
            f"(got {written!r}, expected {WORD!r})",
            file=sys.stderr,
        )
        return 1

    # Byte-level round trip: guards against any encoding surprise
    # (BOM, translated newline, invisible characters) that a text-mode
    # read might hide. The file must be exactly WORD's UTF-8 bytes.
    try:
        with open(output_path, "rb") as f:
            written_bytes = f.read()
    except OSError as exc:
        print(f"error: could not read back {output_path}: {exc}", file=sys.stderr)
        return 1

    if written_bytes != WORD.encode("utf-8"):
        print(
            f"error: entry.txt bytes {written_bytes!r} do not match "
            f"the word's UTF-8 bytes {WORD.encode('utf-8')!r}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
