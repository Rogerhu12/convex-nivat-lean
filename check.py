"""Verify the published source snapshot without invoking Lean or mathlib.

The independent Lean statement and transitive axiom check are built by CI.
This script checks that CI is building exactly the locally audited sources.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from measure import uncomment


ROOT = Path(__file__).resolve().parent
TERMINAL = "NivatTrial.TheoremB"
MODULE_COUNT = 219
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|native_decide)\b")
PROJECT_IMPORT = re.compile(r"\bNivatTrial\.[A-Za-z][A-Za-z0-9_]*\b")
IMPORT_LINE = re.compile(r"^[ \t]*import[ \t]+([^\r\n]+)", re.MULTILINE)
PRIVATE_KEY = re.compile(
    rb"-----BEGIN (?:RSA |OPENSSH |EC |DSA |ENCRYPTED )?PRIVATE KEY-----"
)
ISSUED_TOKEN = re.compile(
    rb"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|"
    rb"github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{30,})\b"
)


class CheckError(RuntimeError):
    """A reproducibility or source-integrity requirement failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def read_json(path: Path) -> dict:
    try:
        result = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CheckError(f"Cannot read JSON {path}: {exc}") from exc
    require(isinstance(result, dict), f"Expected a JSON object: {path}")
    return result


def without_strings(source: str) -> str:
    """Blank ordinary Lean string contents, retaining line breaks.

    `uncomment` first removes nested block and line comments while respecting
    quoted text. This second pass prevents words in diagnostic strings from
    being mistaken for proof commands.
    """
    out: list[str] = []
    quoted = False
    i = 0
    while i < len(source):
        ch = source[i]
        if not quoted:
            if ch == '"':
                quoted = True
                out.append(" ")
            else:
                out.append(ch)
            i += 1
        elif ch == "\\":
            out.append(" ")
            i += 1
            if i < len(source):
                out.append("\n" if source[i] == "\n" else " ")
                i += 1
        elif ch == '"':
            quoted = False
            out.append(" ")
            i += 1
        else:
            out.append("\n" if ch == "\n" else " ")
            i += 1
    require(not quoted, "Unclosed Lean string")
    return "".join(out)


def lean_code(path: Path) -> str:
    try:
        return uncomment(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise CheckError(f"Cannot parse {path}: {exc}") from exc


def check_shortcuts_text(source: str, label: str = "Lean source") -> str:
    try:
        code = uncomment(source)
    except ValueError as exc:
        raise CheckError(f"Cannot parse {label}: {exc}") from exc
    forbidden = FORBIDDEN.search(without_strings(code))
    if forbidden:
        raise CheckError(f"Forbidden Lean shortcut {forbidden.group()} in {label}")
    return code


def check_shortcuts(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise CheckError(f"Cannot read {path}: {exc}") from exc
    return check_shortcuts_text(source, str(path))


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_digest(name: str, data: bytes, expected: str) -> None:
    require(hashlib.sha256(data).hexdigest() == expected,
            f"Source hash mismatch: {name}")


def module_paths(root: Path) -> dict[str, Path]:
    directory = root / "NivatTrial"
    require(directory.is_dir() and not directory.is_symlink(),
            "Missing or symlinked NivatTrial source directory")
    nested = [path for path in directory.rglob("*.lean") if path.parent != directory]
    require(not nested, f"Unexpected nested mathematical sources: {nested}")
    return {"NivatTrial." + path.stem: path
            for path in sorted(directory.glob("*.lean"))}


def validate_source_files(root: Path, expected: dict[str, str]) -> dict[str, Path]:
    """Check exact module set, raw bytes and forbidden commands."""
    require(isinstance(expected, dict), "source_sha256 must be a dictionary")
    require(all(isinstance(k, str) and isinstance(v, str) and
                re.fullmatch(r"[0-9a-f]{64}", v) for k, v in expected.items()),
            "Malformed source_sha256 mapping")
    modules = module_paths(root)
    require(set(modules) == set(expected),
            "Mathematical source set differs from the audited module set: "
            f"missing={sorted(set(expected) - set(modules))}, "
            f"extra={sorted(set(modules) - set(expected))}")
    for name, path in modules.items():
        require(not path.is_symlink(), f"Source is a symlink: {path}")
        validate_digest(name, path.read_bytes(), expected[name])
        check_shortcuts(path)
    return modules


def dependencies(path: Path) -> set[str]:
    code = without_strings(lean_code(path))
    return {name for clause in IMPORT_LINE.findall(code)
            for name in PROJECT_IMPORT.findall(clause)}


def validate_dependency_graph(graph: dict[str, set[str]], terminal: str = TERMINAL) -> None:
    require(terminal in graph, f"Missing terminal module: {terminal}")
    done: set[str] = set()
    active: set[str] = set()

    def visit(name: str) -> None:
        require(name in graph, f"Missing imported project module: {name}")
        require(name not in active, f"Circular project import at {name}")
        if name in done:
            return
        active.add(name)
        for dep in graph[name]:
            visit(dep)
        active.remove(name)
        done.add(name)

    visit(terminal)
    require(done == set(graph),
            f"Terminal import closure omits: {sorted(set(graph) - done)}")


def validate_terminal_closure(modules: dict[str, Path], terminal: str = TERMINAL) -> None:
    validate_dependency_graph({name: dependencies(path) for name, path in modules.items()},
                              terminal)


def source_counts(modules: dict[str, Path]) -> tuple[list[dict], int, int]:
    rows: list[dict] = []
    for path in sorted(modules.values()):
        source = path.read_text(encoding="utf-8-sig")
        code = uncomment(source)
        rows.append({"file": path.name, "total_lines": len(source.splitlines()),
                     "code_lines": sum(bool(line.strip()) for line in code.splitlines())})
    return (rows, sum(row["code_lines"] for row in rows),
            sum(row["total_lines"] for row in rows))


def validate_count_rows(actual_rows: list[dict], audited_rows: object) -> None:
    """Compare every file's counts independently of OS-specific path order."""
    require(isinstance(audited_rows, list), "Original audit has no file count rows")

    def by_filename(rows: list[dict], label: str) -> dict[str, dict]:
        require(all(isinstance(row, dict) and isinstance(row.get("file"), str)
                    for row in rows), f"Malformed {label} file count row")
        names = [row["file"] for row in rows]
        require(len(names) == len(set(names)), f"Duplicate {label} file count row")
        return {row["file"]: row for row in rows}

    require(by_filename(actual_rows, "local") == by_filename(audited_rows, "audited"),
            "Source line counts disagree with original audit report")


def validate_original_report(provenance: dict, report: dict,
                             modules: dict[str, Path]) -> None:
    expected = provenance["source_sha256"]
    require(report.get("success") is True, "Original build report was not successful")
    require(report.get("roots") == [TERMINAL] and
            report.get("scope") == "import-closure",
            "Original report is not the terminal import-closure audit")
    require(report.get("sources_sha256") == expected,
            "Provenance hashes disagree with original audit report")
    require(report.get("lean") == provenance.get("lean") and
            report.get("mathlib_commit") == provenance.get("mathlib_commit"),
            "Lean/mathlib versions disagree with original audit report")
    rows, code_lines, total_lines = source_counts(modules)
    require(provenance.get("code_lines") == code_lines and
            provenance.get("total_lines") == total_lines,
            "Source line counts disagree with provenance")
    counts = report.get("counts")
    require(isinstance(counts, dict) and
            counts.get("code_lines") == code_lines and
            counts.get("total_lines") == total_lines,
            "Source line counts disagree with original audit report")
    validate_count_rows(rows, counts.get("files"))
    checks = report.get("checks")
    require(isinstance(checks, list), "Original audit has no module checks")
    successful = [item.get("module") for item in checks
                  if isinstance(item, dict) and item.get("exit_code") == 0]
    require(len(successful) == len(checks) and len(set(successful)) == len(checks),
            "Original audit contains failed or duplicate checks")
    require(set(successful) == set(modules) |
            {"FinalTheoremB", "FinalTheoremBAxioms"},
            "Original audit checks do not cover exactly this terminal closure")


def validate_tracked_names(paths: set[str], modules: dict[str, Path]) -> None:
    math_paths = {f"NivatTrial/{name.removeprefix('NivatTrial.')}.lean"
                  for name in modules}
    require(math_paths <= paths,
            f"Untracked mathematical sources: {sorted(math_paths - paths)}")
    for name in paths:
        parts = [part.lower() for part in Path(name).parts]
        base = parts[-1]
        require(not set(parts) & {".lake", "__pycache__", ".mypy_cache",
                                  ".pytest_cache", "cache", "caches"},
                f"Tracked build cache: {name}")
        require(not (base.endswith((".olean", ".ilean", ".olean.hash",
                                     ".ilean.hash"))),
                f"Tracked Lean build product: {name}")
        require(not (base in {".env", "id_rsa", "id_ed25519", "credentials",
                              "credentials.json", "secret.json", "secrets.json",
                              "token.txt", "password.txt"} or
                     (base.startswith(".env.") and base != ".env.example") or
                     base.endswith((".pem", ".p12", ".pfx", ".key")) or
                     "secret" in parts),
                f"Tracked secret-like file: {name}")


def git_tracked_paths(root: Path) -> set[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=root,
                            capture_output=True, check=False)
    require(result.returncode == 0,
            "Cannot list Git-tracked files; initialize the release repository first")
    return {item.decode("utf-8") for item in result.stdout.split(b"\0") if item}


def validate_tracked_contents(root: Path, paths: set[str]) -> None:
    for name in paths:
        path = root / name
        require(path.is_file(), f"Tracked file is missing: {name}")
        data = path.read_bytes()
        require(not PRIVATE_KEY.search(data) and not ISSUED_TOKEN.search(data),
                f"Tracked file contains a private key or credential-shaped token: {name}")


def validate_release(root: Path = ROOT, check_git: bool = True) -> None:
    provenance = read_json(root / "source-provenance.json")
    require(provenance.get("module_count") == MODULE_COUNT,
            f"Release must contain exactly {MODULE_COUNT} audited modules")
    expected = provenance.get("source_sha256")
    require(isinstance(expected, dict) and len(expected) == MODULE_COUNT,
            "Provenance must list exactly 219 modules")
    report_name = provenance.get("original_report")
    require(isinstance(report_name, str) and report_name,
            "Missing original_report path in provenance")
    report_path = (root / report_name).resolve()
    require(report_path.is_relative_to(root.resolve()),
            "Original report path escapes the release directory")
    require(report_path.is_file() and not report_path.is_symlink(),
            "Original audit report is missing or symlinked")
    report = read_json(report_path)
    top_level = {path.name for path in root.glob("*.lean")}
    require(top_level == {"NivatTrial.lean", "Statements.lean", "Audit.lean"},
            f"Unexpected top-level Lean sources: {sorted(top_level)}")
    modules = validate_source_files(root, expected)
    validate_terminal_closure(modules)
    validate_original_report(provenance, report, modules)
    for path in root.rglob("*.lean"):
        if not {".git", ".lake"} & set(path.relative_to(root).parts):
            check_shortcuts(path)
    if check_git:
        tracked = git_tracked_paths(root)
        validate_tracked_names(tracked, modules)
        validate_tracked_contents(root, tracked)


def main() -> int:
    try:
        validate_release()
    except CheckError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {MODULE_COUNT} byte-identical audited modules, complete terminal "
          "closure, no proof shortcuts or tracked secrets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
