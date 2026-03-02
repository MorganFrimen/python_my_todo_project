from datetime import datetime
from storage.tasks_db import active_tasks
from storage.persistence import save_all # Импортируем сохранение


def add_task(title, description, deadline, priority="Средний"):
    # Получаем текущее время и форматируем его в красивую строку
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    new_item = {
        "title": title, 
        "description": description, 
        "status": "Ожидает",
        "created_at": now,  # Новый ключ
        "deadline": deadline,
        "priority": priority  # Новый ключ
    }

    active_tasks.append(new_item)
    save_all() # Сохраняем в файл сразу после добавления