#!/usr/bin/env python
import os
import sys
import shutil


def create_log_dirs():
    """Создаёт папки для логов при старте проекта"""
    log_dirs = ['log', 'logs']
    for dir_name in log_dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"Папка {dir_name} создана или уже существует")
        except Exception as e:
            print(f"Ошибка при создании папки {dir_name}: {e}")


def setup_media_files():
    """Копирует системные медиафайлы из media_system/ в media/"""
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_src = os.path.join(BASE_DIR, 'media_system')
        media_dst = os.path.join(BASE_DIR, 'media')

        if os.path.exists(media_src):
            if not os.path.exists(media_dst):
                os.makedirs(media_dst, exist_ok=True)

            # Копируем только отсутствующие файлы
            for item in os.listdir(media_src):
                src_path = os.path.join(media_src, item)
                dst_path = os.path.join(media_dst, item)

                if not os.path.exists(dst_path):
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                    print(f"Скопирован: {item}")
        else:
            print(f"Папка-источник {media_src} не найдена")
    except Exception as e:
        print(f"Ошибка при копировании медиафайлов: {e}")


if __name__ == "__main__":
    # Создаём папки для логов
    create_log_dirs()

    # Копируем системные медиафайлы
    setup_media_files()

    # Стандартная инициализация Django
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