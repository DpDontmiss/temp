import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent

    # Run the existing end-to-end test agent
    result = subprocess.run(
        [sys.executable, str(repo_root / "test_agent.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    # Stream output through so users see normal logs
    print(result.stdout, end="")
    print(result.stderr, file=sys.stderr, end="")

    if result.returncode != 0:
        print("check_demo: test_agent.py exited with a non-zero status", file=sys.stderr)
        return result.returncode or 1

    # Look for the Grade Result line
    grade_line = None
    for line in result.stdout.splitlines():
        if line.startswith("Grade Result:"):
            grade_line = line
            break

    if grade_line is None:
        print("check_demo: could not find 'Grade Result:' line in output", file=sys.stderr)
        return 1

    # Extract and parse the JSON payload after 'Grade Result:'
    try:
        _, json_part = grade_line.split("Grade Result:", 1)
        payload = json.loads(json_part.strip())
    except Exception as exc:  # noqa: BLE001
        print(f"check_demo: failed to parse grade JSON: {exc}", file=sys.stderr)
        return 1

    status = payload.get("status")
    if status != "pass":
        print(f"check_demo: grade status is not 'pass' (got {status!r})", file=sys.stderr)
        return 1

    print("check_demo: grade status is 'pass'")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
