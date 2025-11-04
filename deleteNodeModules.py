#!/usr/bin/env python3
"""Compatibility wrapper for running the tool as a script.

This file preserves the original script entrypoint while delegating to the
refactored package code in `cleanup_nodemodule` when available.
"""
from __future__ import annotations
import sys

try:
    from cleanup_nodemodule.cli import main
except Exception:
    # If package not installed, fall back to running the local module.
    # Import by path
    from src.cleanup_nodemodule.cli import main


if __name__ == '__main__':
    # Allow passing CLI args directly when invoking this script
    main(sys.argv[1:])
