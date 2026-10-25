"""Pinned public SDK identity and diagnostic logging policy."""

import logging
import re
import tomllib
from pathlib import Path

from one_memory.hy_runtime_config import (
    HY_MEMORY_DISTRIBUTION,
    HY_MEMORY_VERSION,
    apply_diagnostic_log_level,
    hy_memory_version,
)

DOCUMENT = Path(__file__).resolve().parents[3] / "MEMORY.md"


def test_the_installed_sdk_is_the_pinned_one():
    assert hy_memory_version() == HY_MEMORY_VERSION
    assert HY_MEMORY_DISTRIBUTION == "hy-memory"


def test_the_pin_matches_the_locked_source_commit():
    core = DOCUMENT.parent / "apps/core"
    lock = tomllib.loads((core / "uv.lock").read_text(encoding="utf-8"))
    project = tomllib.loads((core / "pyproject.toml").read_text(encoding="utf-8"))
    requirement = next(
        value
        for value in project["project"]["dependencies"]
        if value.startswith(f"{HY_MEMORY_DISTRIBUTION} @ git+")
    )
    source, commit = requirement.split(" @ git+", 1)[1].rsplit("@", 1)
    assert re.fullmatch(r"[0-9a-f]{40}", commit)
    assert source == "https://github.com/adybag14-cyber/Hy-Memory.git"
    package = next(
        value for value in lock["package"] if value["name"] == HY_MEMORY_DISTRIBUTION
    )
    assert package["version"] == HY_MEMORY_VERSION
    assert package["source"] == {"git": f"{source}?rev={commit}#{commit}"}


def test_info_level_suppresses_noisy_third_party_success_logs():
    names = ("", "one_memory", "httpx", "httpcore", "watchfiles", "jieba")
    previous = {name: logging.getLogger(name).level for name in names}
    try:
        apply_diagnostic_log_level("info")
        assert logging.getLogger("one_memory").level == logging.INFO
        for name in ("httpx", "httpcore", "watchfiles", "jieba"):
            assert logging.getLogger(name).level == logging.WARNING
        apply_diagnostic_log_level("debug")
        for name in ("one_memory", "httpx", "httpcore", "watchfiles", "jieba"):
            assert logging.getLogger(name).level == logging.DEBUG
    finally:
        for name, level in previous.items():
            logging.getLogger(name).setLevel(level)
