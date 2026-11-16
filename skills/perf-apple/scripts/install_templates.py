#!/usr/bin/env python3
"""Install named baseline links to Apple's templates without copying or editing archives."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="apply; otherwise preview")
    args = parser.parse_args()
    developer = Path(os.environ.get("DEVELOPER_DIR") or subprocess.check_output(
        ["xcode-select", "-p"], text=True
    ).strip())
    if developer.suffix == ".app":
        developer = developer / "Contents/Developer"
    contents = developer.parent / "Applications/Instruments.app/Contents"
    recipes = json.loads((Path(__file__).resolve().parents[1] /
                          "assets/capture-recipes.json").read_text())["recipes"]
    destination = Path.home() / "Library/Application Support/Instruments/Templates"
    plan = []
    for name, recipe in recipes.items():
        filename = recipe["template"] + ".tracetemplate"
        source = contents / "Resources/templates" / filename
        if not source.is_file():
            matches = sorted(contents.glob(f"Packages/*/Contents/Templates/{filename}"))
            if len(matches) != 1:
                raise ValueError(f"cannot uniquely locate {filename}; inspect this Xcode")
            source = matches[0]
        target = destination / f"perf-apple-{name}.tracetemplate"
        if target.exists() or target.is_symlink():
            if not target.is_symlink() or target.resolve() != source.resolve():
                raise ValueError(f"existing template left unchanged: {target}")
        plan.append((target, source))
    # Validate the whole plan before making any filesystem changes.
    if args.install:
        destination.mkdir(parents=True, exist_ok=True)
    for target, source in plan:
        if args.install and not target.is_symlink():
            target.symlink_to(source)
        print(f"{target.stem} -> {source.name}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"install-templates: {error}", file=sys.stderr)
        sys.exit(1)
