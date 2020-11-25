#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


""" TO RUN SERVER...
F:\DJANGO GlobalFruits\OrderPage\OrderPageDjango\blog_pos> 

cd ..

cd ..

cd venvOrder

cd OrderVENV

cd Scripts

activate

cd .. 

cd ..

cd ..


cd OrderPageDjango

cd blog_pos

py manage.py runserver

"""

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_pos.settings')
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
