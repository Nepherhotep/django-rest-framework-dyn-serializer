#!/usr/bin/env python
from os.path import dirname

import os
import sys

if __name__ == "__main__":
    current = dirname(dirname(dirname(os.path.abspath(__file__))))
    sys.path.append(current)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sampleproj.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
