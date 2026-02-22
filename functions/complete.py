from storage.tasks_db import active_tasks
from storage.persistence import save_all # Импортируем сохранение

def mark_as_done(number):
    if 0 < number <= len(active_tasks):
        active_tasks[number - 1]["status"] = "Выполнено"
        save_all() # Сохраняем в файл сразу после добавления
        return True
    return False