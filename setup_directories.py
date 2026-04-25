"""
setup_directories.py

Sets up the complete directory structure for the PDDL agent monitoring project.
Safe to run multiple times (idempotent).
"""

from pathlib import Path


DIRECTORIES: list[str] = [
    "pddl/domains",
    "pddl/problems",
    "monitoring/core",
    "monitoring/utils",
    "monitoring/tests",
    "outputs/plans",
    "outputs/results",
    "outputs/logs",
    "experiments/task1",
    "experiments/task2",
    "experiments/task3",
    "experiments/task4",
    "experiments/task5",
    "docs/findings",
    "docs/reports",
    "scripts",
]

INIT_FILES: list[str] = [
    "monitoring/__init__.py",
    "monitoring/core/__init__.py",
    "monitoring/utils/__init__.py",
    "monitoring/tests/__init__.py",
]


def create_directories(base: Path) -> tuple[list[str], list[str]]:
    """Create all required project directories.

    Args:
        base: The project root path.

    Returns:
        A tuple of (created, failed) directory path strings.
    """
    created: list[str] = []
    failed: list[str] = []

    for rel_path in DIRECTORIES:
        target = base / rel_path
        try:
            target.mkdir(parents=True, exist_ok=True)
            created.append(rel_path)
            print(f"  [dir]  {rel_path}")
        except OSError as exc:
            print(f"  [warn] Could not create '{rel_path}': {exc}")
            failed.append(rel_path)

    return created, failed


def create_init_files(base: Path) -> tuple[int, int]:
    """Create required Python package __init__.py files.

    Args:
        base: The project root path.

    Returns:
        A tuple of (created_count, failed_count).
    """
    created = 0
    failed = 0

    for rel_path in INIT_FILES:
        target = base / rel_path
        try:
            if not target.exists():
                target.touch()
                print(f"  [file] {rel_path}")
            created += 1
        except OSError as exc:
            print(f"  [warn] Could not create '{rel_path}': {exc}")
            failed += 1

    return created, failed


def verify_structure(base: Path) -> tuple[int, int]:
    """Verify that all expected directories and files exist.

    Args:
        base: The project root path.

    Returns:
        A tuple of (dirs_ok, files_ok) counts.
    """
    dirs_ok = sum(1 for d in DIRECTORIES if (base / d).is_dir())
    files_ok = sum(1 for f in INIT_FILES if (base / f).is_file())
    return dirs_ok, files_ok


def setup(base: Path | None = None) -> bool:
    """Run the full project setup.

    Args:
        base: Project root. Defaults to the directory containing this script.

    Returns:
        True if all directories and files were created/verified successfully,
        False if any errors occurred.
    """
    if base is None:
        base = Path(__file__).parent.resolve()

    print(f"\nSetting up project structure in: {base}\n")

    print("Creating directories...")
    created_dirs, failed_dirs = create_directories(base)

    print("\nCreating Python package files...")
    created_files, failed_files = create_init_files(base)

    print("\nVerifying structure...")
    dirs_ok, files_ok = verify_structure(base)

    all_ok = not failed_dirs and not failed_files

    print("\n" + "=" * 50)
    print("Setup Report")
    print("=" * 50)
    print(f"  \u2713 Created directories: {created_dirs}")
    print(f"  \u2713 Created Python package files: {created_files}")
    print(f"  \u2713 Total directories verified: {dirs_ok}/{len(DIRECTORIES)}")
    print(f"  \u2713 Total files verified: {files_ok}/{len(INIT_FILES)}")

    if all_ok:
        print("\n  Project structure verified and ready.\n")
    else:
        print(
            f"\n  [warn] Setup completed with issues "
            f"({len(failed_dirs)} dir(s) and {failed_files} file(s) failed).\n"
        )

    return all_ok


if __name__ == "__main__":
    success = setup()
    raise SystemExit(0 if success else 1)
