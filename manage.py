#!/usr/bin/env python
"""Django command-line entry point."""

import os
import sys


def main() -> None:
    """Run Django's command-line utility."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django ist nicht installiert. Nutze: pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
