#!/usr/bin/env python3
"""
fix_csv_linebreaks.py  –  v2 (with encoding support)

• Merges rows that were split by stray new-lines.
• Writes the cleaned file in UTF-8-BOM so Excel shows special characters.

USAGE
-----
python fix_csv_linebreaks.py broken.csv cleaned.csv            # defaults
python fix_csv_linebreaks.py broken.csv cleaned.csv latin-1    # custom source enc
python fix_csv_linebreaks.py broken.csv cleaned.csv utf-8 cp1252  cp1252 target
"""
import re
import sys

# ----- tweak this pattern if another field uniquely marks the start of a row
ROW_START = re.compile(r'^\d{6,},')      # e.g. “123456,”

def fix_csv(src, dst, in_enc="utf-8", out_enc="utf-8-sig"):
    """Read *src* using *in_enc*, glue orphan lines, write *dst* using *out_enc*."""
    with open(src, "r", encoding=in_enc, errors="replace") as fin, \
         open(dst, "w", encoding=out_enc, newline="") as fout:   # newline="" → no doubling

        # header goes through untouched
        header = fin.readline().rstrip("\r\n")
        fout.write(header + "\n")

        buffer = ""
        for line in fin:
            if ROW_START.match(line):                 # looks like a new record
                if buffer:                            # flush previous
                    fout.write(buffer + "\n")
                buffer = line.rstrip("\r\n")
            else:                                     # continuation of current record
                buffer += " " + line.strip("\r\n")

        if buffer:                                    # flush final record
            fout.write(buffer + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: fix_csv_linebreaks.py src.csv dst.csv [src_encoding] [dst_encoding]")
        sys.exit(1)

    src_file, dst_file = sys.argv[1:3]
    src_enc  = sys.argv[3] if len(sys.argv) > 3 else "utf-8"
    dst_enc  = sys.argv[4] if len(sys.argv) > 4 else "utf-8-sig"

    fix_csv(src_file, dst_file, src_enc, dst_enc)
    print(f"✔ Wrote {dst_file} in {dst_enc}")
