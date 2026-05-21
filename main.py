import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def start_application():
    try:
        from gui.app import main as run_gui
        run_gui()
        
    except ImportError as e:
        print(f"\n Не удалось запустить проект: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n Программа успешно остановлена.")
        sys.exit(0)

if __name__ == "__main__":
    start_application()