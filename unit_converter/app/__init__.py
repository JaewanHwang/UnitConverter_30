"""app — 조립 및 CLI 진입 (I/O 경계)."""

from unit_converter.app.assembler import build_registry
from unit_converter.app.cli import render, run_cli

__all__ = ["build_registry", "render", "run_cli"]
