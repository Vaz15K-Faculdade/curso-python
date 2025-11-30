import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
import qasync

from frontend.main_window import MainWindow
from frontend.styles import get_global_stylesheet
import asyncio


def main():
    """Função principal da aplicação"""    
    app = QApplication(sys.argv)
    app.setApplicationName("Tessera")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Vazz")
    
    app.setStyleSheet(get_global_stylesheet())
    
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = MainWindow()
    window.show()
    
    try:
        # Executa o loop de eventos
        with loop:
            loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erro na aplicação: {e}")


if __name__ == "__main__":
    main()
