"""Cross-platform path prefix remapping via JCODEMUNCH_PATH_MAP."""

import logging
import os

logger = logging.getLogger(__name__)

ENV_VAR = "JCODEMUNCH_PATH_MAP"


def parse_path_map() -> list[tuple[str, str]]:
    """Parse JCODEMUNCH_PATH_MAP into (original, replacement) pairs.

    Format: orig1=new1,orig2=new2,...
    Splits on the last '=' so paths containing '=' work correctly.
    Returns [] when the env var is unset or empty.
    Malformed entries (no '=', empty orig, empty new) are skipped with a WARNING.
    """
    raw = os.environ.get(ENV_VAR, "").strip()
    if not raw:
        return []

    pairs: list[tuple[str, str]] = []
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if "=" not in entry:
            logger.warning("JCODEMUNCH_PATH_MAP: skipping malformed entry (no '='): %r", entry)
            continue
        orig, new = entry.rsplit("=", 1)
        orig = orig.strip()
        new = new.strip()
        if not orig:
            logger.warning("JCODEMUNCH_PATH_MAP: skipping entry with empty original prefix: %r", entry)
            continue
        if not new:
            logger.warning("JCODEMUNCH_PATH_MAP: skipping entry with empty replacement prefix: %r", entry)
            continue
        pairs.append((orig, new))
    return pairs
