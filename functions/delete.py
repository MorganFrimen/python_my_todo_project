from datetime import datetime
from storage.tasks_db import active_tasks
from storage.history_tasks import archived_tasks
from storage.persistence import save_all # Импортируем сохранение


def move_to_trash(number):
    if 0 < number <= len(active_tasks):
        # Забираем из активных
        item = active_tasks.pop(number - 1)
        
        item["deleted_at"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        # Кладем в историю
        archived_tasks.append(item)
        save_all()
        return item
    return None