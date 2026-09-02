"""Report compressed wheel and uncompressed extension sizes."""

from __future__ import annotations

import argparse
import csv
import zipfile
from pathlib import Path


def wheel(value):
    try:
        label, filename = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected LABEL=WHEEL") from error
    path = Path(filename).expanduser().resolve()
    if not label or not path.is_file():
        raise argparse.ArgumentTypeError(f"invalid wheel: {value}")
    return label, path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", nargs="+", type=wheel)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    fields = (
        "implementation",
        "wheel_bytes",
        "wheel_uncompressed_bytes",
        "dwt_compressed_bytes",
        "dwt_uncompressed_bytes",
    )
    with args.output.open("x", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fields, lineterminator="\n")
        writer.writeheader()
        for label, path in args.wheel:
            with zipfile.ZipFile(path) as archive:
                files = archive.infolist()
                extensions = [
                    item
                    for item in files
                    if "/_dwt." in item.filename
                    and item.filename.endswith((".so", ".pyd"))
                ]
                if len(extensions) != 1:
                    raise ValueError(
                        f"expected one _dwt extension in {path}, "
                        f"found {len(extensions)}"
                    )
                extension = extensions[0]
                writer.writerow(
                    {
                        "implementation": label,
                        "wheel_bytes": path.stat().st_size,
                        "wheel_uncompressed_bytes": sum(
                            item.file_size for item in files
                        ),
                        "dwt_compressed_bytes": extension.compress_size,
                        "dwt_uncompressed_bytes": extension.file_size,
                    }
                )


if __name__ == "__main__":
    main()
