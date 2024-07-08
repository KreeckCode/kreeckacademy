#!/usr/bin/env python
import os
import sys
import environ

def main():
    # Load environment variables
    environ.Env.read_env()

    # Set the appropriate settings module
    settings_module = 'SMS.settings_prod' if 'DJANGO_SETTINGS_MODULE' in os.environ else 'SMS.settings_dev'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
