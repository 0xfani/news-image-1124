"""news-image-20261124 entry: puts the prepared front page at /output/entry.png.

The picture (entry.png, kept next to this file) sums up the world news of
Tuesday 24 November 2026. The sandbox has no network, so the program only
validates the file and copies its bytes unchanged: both runs write the same bytes.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024  # the bounty's 1 MiB cap
MAX_SIDE = 1024  # neither side may exceed 1024 pixels
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def output_dir():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target, exist_ok=True)
    return target


def check_png_size(data):
    """Read width and height from the IHDR chunk that must follow the signature."""
    if data[12:16] != b"IHDR":
        sys.exit("entry.png has no IHDR chunk right after the PNG signature")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        sys.exit(f"entry.png is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} limit")
    return width, height


def load_image(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes, over the {MAX_BYTES}-byte cap")
    if data.startswith(PNG_MAGIC):
        check_png_size(data)
    elif not data.startswith(JPEG_MAGIC):
        sys.exit("entry.png does not start with PNG or JPEG magic bytes")
    return data


def main():
    data = load_image(SOURCE)
    destination = os.path.join(output_dir(), "entry.png")
    with open(destination, "wb") as handle:
        handle.write(data)
    print(f"wrote {len(data)} bytes to {destination}")


if __name__ == "__main__":
    main()
