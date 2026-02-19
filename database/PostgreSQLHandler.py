"""
Обработчик базы данных PostgreSQL с Django ORM
"""
import os
import sys
import django
from pathlib import Path
from typing import List, Optional, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.utils import OperationalError, IntegrityError, ProgrammingError

# Добавляем текущую директорию в путь Python
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config')

try:
    django.setup()
    from .models import Customer
    from django.db import models as django_models
    DJANGO_SETUP = True
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    DJANGO_SETUP = False
    Customer = None
    django_models = None

def save_articles(articles):
    saved_count = 0
    for article in articles:
        # Создаем новую запись без проверки на совпадение заголовка
        Customer.Blog.objects.create(title=article.title, text=article.text, author='Автор')  # укажите автор при необходимости
        saved_count += 1
    return saved_count

def setup_database():
    """Настройка базы данных: создание и применение миграций."""
    if not DJANGO_SETUP:
        print("❌ Django не настроен")
        return False

    from django.core.management import call_command

    print("🔄 Инициализация таблиц в базе данных...")

    # 0. Убедиться, что пакет database.migrations существует (Django иначе не видит миграции)
    migrations_dir = Path(__file__).parent / 'migrations'
    migrations_dir.mkdir(exist_ok=True)
    (migrations_dir / '__init__.py').touch()

    # 1. Создать миграции для приложения database (создаёт файлы в database/migrations/)
    try:
        print("  Создание миграций...")
        call_command('makemigrations', 'database', verbosity=2)
    except Exception as e:
        print(f"⚠️ Ошибка создания миграций: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 2. Применить миграции к БД
    try:
        call_command('migrate', 'database', verbosity=2)
    except Exception as e:
        print(f"❌ Ошибка применения миграций: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("✅ Таблицы в базе данных созданы/обновлены")
    return True

