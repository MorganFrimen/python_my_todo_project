import json
import os
# Импортируем списки напрямую из модулей
from storage.tasks_db import active_tasks
from storage.history_tasks import archived_tasks

# Укажем пути относительно папки storage
current_dir = os.path.dirname(__file__)
DB_FILE = os.path.join(current_dir, "data.json")
HISTORY_FILE = os.path.join(current_dir, "history.json")

def save_all():
    """Сохраняет текущие списки в JSON"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(active_tasks, f, ensure_ascii=False, indent=4)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(archived_tasks, f, ensure_ascii=False, indent=4)

def load_all():
    """Безопасная загрузка данных"""
    # Очищаем списки перед загрузкой, чтобы не дублировать данные
    active_tasks.clear()
    archived_tasks.clear()

    # Проверяем наличие файла с задачами
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                active_tasks.extend(data)
        except (json.JSONDecodeError, ValueError):
            print("Файл data.json поврежден, создаем новый.")
    
    # Проверяем наличие файла с историей
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                archived_tasks.extend(data)
        except (json.JSONDecodeError, ValueError):
            print("Файл history.json поврежден.")