# main.py
import time
from ui.app_window import TodoApp
from storage.persistence import load_all

def main():
    # 1. Сначала загружаем данные
    load_all()
    
    # 2. Небольшая пауза перед графикой (решает проблемы с зависанием потока)
    time.sleep(0.2) 
    
    try:
        app = TodoApp()
        app.mainloop()
    except Exception as e:
        print(f"Ошибка при запуске: {e}")

if __name__ == "__main__":
    main()