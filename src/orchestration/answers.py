import re
from typing import Optional


_ANSWER_REGEX = re.compile(r"^\s*(?:final\s+answer|answer)\s*:\s*(.+?)\s*$", re.IGNORECASE)


def extract_answer(text: str) -> Optional[str]:
    found = None
    for line in text.splitlines():
        clean = line.replace("*", "")
        m = _ANSWER_REGEX.match(clean)
        if m:
            found = m.grou1p(1).strip()
    return found


def normalize_answer(answer: Optional[str]) -> Optional[str]:
    if answer is None:
        return None
    s = answer.strip().lower()
    s = s.replace("$", "").replace(",", "").rstrip(".").strip()
    try:
        return f"{float(s):.10g}"
    except ValueError:
        return " ".join(s.split())