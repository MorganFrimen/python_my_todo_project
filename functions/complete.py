from datetime import datetime
from storage.tasks_db import active_tasks
from storage.persistence import save_all  

def mark_as_done(number):
    if 0 < number <= len(active_tasks):
        task = active_tasks[number - 1]
        
        # 1. Логика проверки просрочки
        try:
            today = datetime.now().date()
            # Убедись, что формат %d.%m.%Y совпадает с твоим календарем!
            deadline_date = datetime.strptime(task.get('deadline'), "%d.%m.%Y").date()
            
            if deadline_date < today:
                task['completion_status'] = "С опозданием"
            else:
                task['completion_status'] = "Вовремя"
        except Exception as e:
            # Если даты нет или формат не подошел
            task['completion_status'] = "Без дедлайна"
            
        # 2. Меняем статус
        task["status"] = "Выполнено"
        
        # 3. СОХРАНЯЕМ ИЗМЕНЕНИЯ В ФАЙЛ
        save_all() 
        
        return True
    return False