"""
check_fastdownward_dependencies.py

Checks if all required dependencies for building FastDownward are installed.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def check_command_exists(command: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(command) is not None


def get_version(command: str, args: list[str] = None) -> str | None:
    """Get the version of a command."""
    if args is None:
        args = ["--version"]
    try:
        result = subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.split("\n")[0] if result.stdout else None
    except Exception:
        return None


def main() -> None:
    """Check FastDownward dependencies."""
    print("FastDownward Dependency Checker")
    print("=" * 60)
    print()

    dependencies: dict[str, dict[str, bool | str]] = {
        "Python 3": {"required": True, "command": "python"},
        "CMake": {"required": True, "command": "cmake"},
        "MSVC (cl.exe)": {"required": False, "command": "cl.exe"},
        "GCC (g++)": {"required": False, "command": "g++"},
        "NMake": {"required": False, "command": "nmake"},
        "Make": {"required": False, "command": "make"},
    }

    missing_required: list[str] = []
    available_optional: list[str] = []

    for name, info in dependencies.items():
        command = info["command"]
        exists = check_command_exists(command)
        version = get_version(command) if exists else None

        status = "✓" if exists else "✗"
        is_required = info["required"]
        req_text = "(REQUIRED)" if is_required else "(Optional)"

        if exists:
            print(f"{status} {name} {req_text}")
            if version:
                print(f"   {version}")
            if not is_required:
                available_optional.append(name)
        else:
            print(f"{status} {name} {req_text} - NOT FOUND")
            if is_required:
                missing_required.append(name)

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    if not missing_required:
        print("✓ All required dependencies are installed!")
        print()
        print("You can now build FastDownward by running:")
        print("  cd downward")
        print("  python build.py")
    else:
        print(f"✗ Missing {len(missing_required)} required dependencies:")
        for dep in missing_required:
            print(f"  - {dep}")
        print()
        print("To install missing dependencies, see FASTDOWNWARD_SETUP.md")
        return 1

    print()
    if available_optional:
        print(f"Available compilers: {', '.join(available_optional)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
