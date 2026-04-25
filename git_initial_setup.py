"""Initialize Git-ready project structure for the PDDL agent monitoring project."""

from __future__ import annotations

from pathlib import Path
import subprocess


GITIGNORE_ENTRIES: list[str] = [
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    ".venv/",
    "venv/",
    "*.egg-info/",
    "downward/",
    "outputs/plans/*.txt",
    "outputs/logs/*.log",
]

DIRECTORIES_TO_TRACK: list[str] = [
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

INIT_FILES: dict[str, str] = {
    "monitoring/__init__.py": '"""Monitoring package."""\n',
    "monitoring/core/__init__.py": '"""Core monitoring logic."""\n',
    "monitoring/utils/__init__.py": '"""Utility helpers for monitoring."""\n',
    "monitoring/tests/__init__.py": '"""Tests for monitoring components."""\n',
}


def ensure_gitignore(project_root: Path) -> tuple[bool, list[str]]:
    """Ensure .gitignore exists and contains required entries.

    Returns:
        tuple[bool, list[str]]: success flag and list of entries added.
    """
    success = True
    added_entries: list[str] = []
    gitignore_path = project_root / ".gitignore"

    try:
        if not gitignore_path.exists():
            gitignore_path.write_text("", encoding="utf-8")
            print("[ok] Created .gitignore")
        else:
            print("[ok] Found existing .gitignore")
    except OSError as exc:
        print(f"[warn] Could not create/read .gitignore: {exc}")
        return False, added_entries

    try:
        existing_lines = gitignore_path.read_text(encoding="utf-8").splitlines()
        existing_set = {line.strip() for line in existing_lines if line.strip()}

        for entry in GITIGNORE_ENTRIES:
            if entry not in existing_set:
                existing_lines.append(entry)
                added_entries.append(entry)

        gitignore_path.write_text("\n".join(existing_lines).rstrip() + "\n", encoding="utf-8")

        if added_entries:
            print(f"[ok] Added {len(added_entries)} .gitignore entries")
        else:
            print("[ok] .gitignore already contains required entries")
    except OSError as exc:
        print(f"[warn] Could not update .gitignore: {exc}")
        success = False

    return success, added_entries


def create_gitkeep_files(project_root: Path) -> tuple[bool, list[str]]:
    """Create .gitkeep files for directories that are empty.

    Returns:
        tuple[bool, list[str]]: success flag and list of .gitkeep paths created.
    """
    success = True
    created_keeps: list[str] = []

    for relative_dir in DIRECTORIES_TO_TRACK:
        target_dir = project_root / relative_dir

        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print(f"[warn] Could not ensure directory {relative_dir}: {exc}")
            success = False
            continue

        try:
            has_contents = any(target_dir.iterdir())
            if not has_contents:
                gitkeep_path = target_dir / ".gitkeep"
                gitkeep_path.touch(exist_ok=True)
                created_keeps.append(str(gitkeep_path.relative_to(project_root)))
                print(f"[ok] Created {gitkeep_path.relative_to(project_root)}")
            else:
                print(f"[ok] Directory not empty, skip .gitkeep: {relative_dir}")
        except OSError as exc:
            print(f"[warn] Could not inspect/create .gitkeep in {relative_dir}: {exc}")
            success = False

    return success, created_keeps


def ensure_init_files(project_root: Path) -> tuple[bool, list[str]]:
    """Ensure package __init__.py files exist.

    Returns:
        tuple[bool, list[str]]: success flag and list of files created.
    """
    success = True
    created_files: list[str] = []

    for relative_file, contents in INIT_FILES.items():
        target_file = project_root / relative_file

        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            if not target_file.exists():
                target_file.write_text(contents, encoding="utf-8")
                created_files.append(relative_file)
                print(f"[ok] Created {relative_file}")
            else:
                print(f"[ok] Exists: {relative_file}")
        except OSError as exc:
            print(f"[warn] Could not create {relative_file}: {exc}")
            success = False

    return success, created_files


def run_git_command(project_root: Path, args: list[str]) -> tuple[bool, str]:
    """Run a git command and return success with combined output."""
    try:
        result = subprocess.run(
            args,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode == 0, output.strip()
    except OSError as exc:
        return False, f"OS error running {' '.join(args)}: {exc}"


def create_initial_commit(project_root: Path) -> tuple[bool, str]:
    """Stage all files and create the initial commit.

    Returns:
        tuple[bool, str]: success flag and status message.
    """
    add_ok, add_output = run_git_command(project_root, ["git", "add", "."])
    if not add_ok:
        message = f"git add failed. {add_output}" if add_output else "git add failed."
        print(f"[warn] {message}")
        return False, message

    commit_ok, commit_output = run_git_command(
        project_root,
        ["git", "commit", "-m", "Initial project structure setup"],
    )

    if commit_ok:
        message = "Initial commit created: Initial project structure setup"
        print(f"[ok] {message}")
        return True, message

    lower_output = commit_output.lower()
    if "nothing to commit" in lower_output or "working tree clean" in lower_output:
        message = "No commit created because there were no new changes to commit."
        print(f"[warn] {message}")
        return False, message

    message = f"git commit failed. {commit_output}" if commit_output else "git commit failed."
    print(f"[warn] {message}")
    return False, message


def print_final_status(
    gitignore_added: list[str],
    gitkeeps_created: list[str],
    init_files_created: list[str],
    commit_message: str,
    success: bool,
) -> None:
    """Print a summary of setup actions and result."""
    print("\n" + "=" * 60)
    print("Final Status")
    print("=" * 60)
    print(f".gitignore entries added: {len(gitignore_added)}")
    print(f".gitkeep files created: {len(gitkeeps_created)}")
    print(f"__init__.py files created: {len(init_files_created)}")
    print(f"Git commit status: {commit_message}")
    print(f"Overall success: {success}")


def setup_git_initial(project_root: Path | None = None) -> bool:
    """Run full setup for Git initialization and project tracking.

    Returns:
        bool: True if all steps succeeded, False if any step had warnings/errors.
    """
    root = project_root or Path(__file__).resolve().parent
    print(f"Project root: {root}")

    all_success = True

    gitignore_ok, gitignore_added = ensure_gitignore(root)
    if not gitignore_ok:
        all_success = False

    gitkeep_ok, gitkeeps_created = create_gitkeep_files(root)
    if not gitkeep_ok:
        all_success = False

    init_ok, init_files_created = ensure_init_files(root)
    if not init_ok:
        all_success = False

    commit_ok, commit_message = create_initial_commit(root)
    if not commit_ok:
        all_success = False

    print_final_status(
        gitignore_added=gitignore_added,
        gitkeeps_created=gitkeeps_created,
        init_files_created=init_files_created,
        commit_message=commit_message,
        success=all_success,
    )

    return all_success


if __name__ == "__main__":
    result = setup_git_initial()
    print(f"Script completed with success={result}")
