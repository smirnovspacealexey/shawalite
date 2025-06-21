#!/usr/bin/env python
import os
import sys


def create_log_dirs():
    """Создаёт папки для логов при старте проекта"""
    log_dirs = ['log', 'logs']
    for dir_name in log_dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"Папка {dir_name} создана или уже существует")
        except Exception as e:
            print(f"Ошибка при создании папки {dir_name}: {e}")


if __name__ == "__main__":
    # Создаём папки для логов перед инициализацией Django
    create_log_dirs()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shawarma.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
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