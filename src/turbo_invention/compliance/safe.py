"""Five Safes gate (Safe People / Project / Setting / Data / Outputs)."""
from __future__ import annotations


def five_safes_gate(*, people: bool, project: bool, setting: bool,
                    data: bool, outputs: bool) -> None:
    failed = [name for name, ok in
              [("people", people), ("project", project), ("setting", setting),
               ("data", data), ("outputs", outputs)] if not ok]
    if failed:
        raise PermissionError(
            f"Five Safes gate refused export: not asserted -> {failed}. "
            "See docs/compliance.md.")
