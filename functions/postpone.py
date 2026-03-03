# -*- coding: utf-8 -*-
from storage.tasks_db import active_tasks

def postpone_task(number, new_deadline):
    if 0 < number <= len(active_tasks):
        active_tasks[number - 1]['deadline'] = new_deadline
        # Если продлили, убираем статус просрочки (даем второй шанс)
        active_tasks[number - 1]['was_expired'] = False 
        return True
    return False