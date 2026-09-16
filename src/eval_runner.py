from __future__ import annotations

import json
import sys
from pathlib import Path


def stub_agent(text: str) -> str:
    """Deterministic stand-in — swap for real agent later."""
    t = text.strip().lower()
    if "cancel" in t or "stop" in t or "interrupt" in t:
        return "STOP: acknowledged cancel"
    if "hours" in t or "open" in t:
        return "We are open 9am–5pm Mountain."
    if "transfer" in t or "human" in t or "person" in t:
        return "TRANSFER: connecting you to a human"
    if not t:
        return "ERROR: empty input"
    return f"ACK: {text.strip()[:120]}"


def check(case: dict, output: str) -> tuple[bool, str]:
    expect = case.get("expect") or {}
    if "contains" in expect:
        ok = expect["contains"].lower() in output.lower()
        return ok, f"contains:{expect['contains']!r}"
    if "startswith" in expect:
        ok = output.lower().startswith(expect["startswith"].lower())
        return ok, f"startswith:{expect['startswith']!r}"
    if "equals" in expect:
        ok = output == expect["equals"]
        return ok, "equals"
    return False, "no expect rule"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "cases")
    cases = sorted(root.glob("*.json"))
    if not cases:
        print("no cases found")
        return 2
    passed = 0
    print(f"{'id':<28} {'ok':>4}  detail")
    print(f"{'-'*28} {'-'*4}  ------")
    for path in cases:
        case = json.loads(path.read_text())
        out = stub_agent(case.get("input", ""))
        ok, detail = check(case, out)
        passed += int(ok)
        print(f"{case.get('id', path.stem):<28} {str(ok):>4}  {detail} | {out[:60]}")
    total = len(cases)
    print(f"\n{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
