"""Check CLI version and full startup without allowing modal errors to hang CI."""

import argparse
import pathlib
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", action="store_true")
    args = parser.parse_args()

    if args.bundle:
        if sys.platform == "darwin":
            pattern = "*.app/Contents/MacOS/pyGAPS-gui"
        elif sys.platform == "win32":
            pattern = "pyGAPS-gui v*/pyGAPS-gui.exe"
        else:
            pattern = "pyGAPS-gui v*/pyGAPS-gui"
        executables = list(pathlib.Path("dist").glob(pattern))
        if len(executables) != 1:
            raise RuntimeError(f"Expected one bundled executable, found {executables}")
        command = [str(executables[0].resolve())]
    else:
        executable = shutil.which("pygapsgui", path=str(pathlib.Path(sys.executable).parent))
        if executable is None:
            raise RuntimeError("The pygapsgui console entry point is not installed")
        command = [executable]

    for option in ("--version", "--test"):
        subprocess.run(command + [option], check=True, timeout=90)


if __name__ == "__main__":
    main()
