"""Run balanced end-to-end comparisons across isolated interpreters."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path

from benchmark_case import CASES

HEADER = "implementation,round,case,dtype,layouts,q1_ms,median_ms,q3_ms\n"


def interpreter(value):
    try:
        label, executable = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected LABEL=PYTHON") from error
    path = Path(executable).expanduser().absolute()
    if not label or not path.is_file():
        raise argparse.ArgumentTypeError(f"invalid interpreter: {value}")
    return label, path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--python",
        action="append",
        required=True,
        type=interpreter,
        metavar="LABEL=PYTHON",
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--rounds", type=int, default=6)
    parser.add_argument("--layouts", type=int, default=64)
    parser.add_argument("--cpu", type=int)
    parser.add_argument("--dtype", action="append", choices=("float32", "float64"))
    parser.add_argument("--case", action="append", choices=CASES)
    args = parser.parse_args()

    implementations = dict(args.python)
    if len(implementations) != len(args.python) or len(implementations) < 2:
        parser.error("provide at least two uniquely labelled interpreters")
    if args.rounds < len(implementations):
        parser.error("--rounds must cover every implementation order")

    benchmark = Path(__file__).with_name("benchmark_case.py")
    dtypes = args.dtype or ("float32", "float64")
    cases = args.case or CASES
    environment = os.environ.copy()
    environment.update(
        {
            "MKL_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "PYTHONHASHSEED": "0",
        }
    )

    labels = list(implementations)
    with args.output.open("x", encoding="utf-8") as output:
        output.write(HEADER)
        output.flush()
        for round_number in range(1, args.rounds + 1):
            offset = (round_number - 1) % len(labels)
            order = labels[offset:] + labels[:offset]
            for dtype in dtypes:
                for case in cases:
                    for label in order:
                        command = [
                            implementations[label],
                            benchmark,
                            label,
                            str(round_number),
                            case,
                            dtype,
                            "--layouts",
                            str(args.layouts),
                        ]
                        if args.cpu is not None:
                            command = ["taskset", "-c", str(args.cpu), *command]
                        print(
                            "+ " + shlex.join(map(str, command)),
                            file=sys.stderr,
                            flush=True,
                        )
                        subprocess.run(
                            command,
                            check=True,
                            env=environment,
                            stdout=output,
                            text=True,
                        )
                        output.flush()


if __name__ == "__main__":
    main()
