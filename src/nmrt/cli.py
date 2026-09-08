from __future__ import annotations

import argparse
import json

from nmrt.pipeline.runner import run_recipe


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="nmrt", description="Neuromuscular Research Toolkit")
    sub = p.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run a YAML analysis recipe")
    run.add_argument("recipe")
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        print(json.dumps(run_recipe(args.recipe), indent=2))


if __name__ == "__main__":
    main()
