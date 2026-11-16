#!/usr/bin/env python3
"""Preview or run a scoped xctrace capture using an installed standard template."""

import argparse
import json
import math
from pathlib import Path
import shlex
import subprocess
import sys


def inventory(kind):
    result = subprocess.run(
        ["xcrun", "xctrace", "list", kind], check=True, capture_output=True, text=True
    )
    return {line.strip() for line in result.stdout.splitlines() if line and not line.startswith("==")}


def main():
    recipes = json.loads(
        (Path(__file__).resolve().parents[1] / "assets/capture-recipes.json").read_text()
    )["recipes"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipe", nargs="?", choices=recipes)
    parser.add_argument("--list", action="store_true", help="list workflow recipes")
    parser.add_argument("--template", help="override with an installed standard template")
    parser.add_argument("--instrument", action="append", default=[], help="add one focused instrument")
    parser.add_argument("--show-options", action="store_true", help="inspect options without recording")
    parser.add_argument("--recording-options", type=Path, help="JSON discovered with --show-options")
    parser.add_argument("--device", help="explicit device name or UDID; omitted means this Mac")
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--pid", type=int, help="attach to this process ID")
    target.add_argument("--launch", type=Path, help="launch this executable or app")
    parser.add_argument("--seconds", type=float, default=15, help="bounded recording duration")
    parser.add_argument("--output", type=Path, help="new private .trace path in an existing directory")
    parser.add_argument("--run", action="store_true", help="execute; default only prints the command")
    # Arguments after -- belong only to the launched process, never to a shell.
    argv = sys.argv[1:]
    split = argv.index("--") if "--" in argv else len(argv)
    args = parser.parse_args(argv[:split])
    launch_args = argv[split + 1:]
    if args.list:
        for name, recipe in recipes.items():
            print(f"{name}: {recipe['template']} — {recipe['purpose']}")
        return 0
    if not args.recipe:
        parser.error("choose a recipe or --list")
    recipe = recipes[args.recipe]
    template = args.template or recipe["template"]
    if template not in inventory("templates"):
        parser.error(f"template not installed: {template}; select the intended Xcode/device")
    instruments = list(dict.fromkeys(recipe["instruments"] + args.instrument))
    missing = set(instruments) - inventory("instruments")
    if missing:
        parser.error(f"instruments not installed: {', '.join(sorted(missing))}")
    command = ["xcrun", "xctrace", "record", "--template", template]
    for name in instruments:
        command += ["--instrument", name]
    if args.device:
        command += ["--device", args.device]
    if args.show_options:
        if args.run or args.pid or args.launch or args.output or launch_args or args.recording_options:
            parser.error("--show-options is read-only; omit recording and target arguments")
        return subprocess.run(command + ["--show-recording-options"]).returncode
    if args.pid is None and args.launch is None:
        parser.error("select --pid or --launch; all-process recording is not a recipe default")
    if args.pid is not None and args.pid <= 0:
        parser.error("--pid must be positive")
    if launch_args and not args.launch:
        parser.error("arguments after -- require --launch")
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error("--seconds must be finite and positive")
    if not args.output or args.output.suffix != ".trace":
        parser.error("choose a new --output path ending in .trace")
    if args.output.exists() or args.output.is_symlink():
        parser.error("output already exists; choose a fresh path")
    if not args.output.parent.is_dir():
        parser.error("create the private output directory first")
    if args.launch and not args.launch.exists():
        parser.error("launch target does not exist")
    if args.recording_options:
        if not args.recording_options.is_file():
            parser.error("recording-options file does not exist")
        json.loads(args.recording_options.read_text())
        command += ["--recording-options", str(args.recording_options.resolve())]
    command += ["--time-limit", f"{args.seconds:g}s", "--output", str(args.output.resolve())]
    if args.pid is not None:
        command += ["--attach", str(args.pid)]
    else:
        command += ["--launch", "--", str(args.launch.resolve()), *launch_args]
    print(shlex.join(command), flush=True)
    if args.run:
        # Keep xctrace prompts and exit status visible. Do not silently retry or delete evidence.
        return subprocess.run(command).returncode
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"capture: {error}", file=sys.stderr)
        sys.exit(1)
