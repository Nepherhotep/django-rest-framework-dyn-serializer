#!/usr/bin/env python
from os.path import dirname

import os
import sys

if __name__ == "__main__":
    sample_dir = dirname(os.path.abspath(__file__))
    root = dirname(dirname(sample_dir))
    sys.path.append(root)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sampleproj.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
