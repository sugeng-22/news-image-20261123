#!/usr/bin/env python3
"""make.fun entry for news-image-20261123 (News Image).

Copies the news infographic stored in this repository (entry.png, next
to this file) to /output/entry.png. Standard library only, no network,
fully deterministic: every run writes exactly the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = "/output"
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)


if __name__ == "__main__":
    main()
