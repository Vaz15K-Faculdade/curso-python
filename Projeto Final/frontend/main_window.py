import sys
import asyncio
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                               QWidget, QStackedWidget)
import qasync

from frontend.components.header import HeaderWidget
from frontend.components.login import LoginDialog
from frontend.components.catalog import CatalogWidget
from frontend.components.tickets import MyTicketsWidget
from frontend.components.admin import AdminWidget
from frontend.api.client import APIClient


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_user = None
        
        self.setWindowTitle("Toten Virtual - Sistema de Ingressos")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configura a interface principal"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.header = HeaderWidget()
        main_layout.addWidget(self.header)
        
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        self.catalog_page = CatalogWidget(self.api_client)
        self.my_tickets_page = MyTicketsWidget(self.api_client)
        self.admin_page = AdminWidget(self.api_client)
        
        self.content_stack.addWidget(self.catalog_page)
        self.content_stack.addWidget(self.my_tickets_page)
        self.content_stack.addWidget(self.admin_page)
        
        self.content_stack.setCurrentWidget(self.catalog_page)
        
    def setup_connections(self):
        """Configura as conexões de sinais"""
        self.header.login_requested.connect(self.show_login_dialog)
        self.header.logout_requested.connect(self.logout)
        self.header.catalog_clicked.connect(self.show_catalog)
        self.header.my_tickets_clicked.connect(self.show_my_tickets)
        self.header.admin_clicked.connect(self.show_admin)
        
    def show_login_dialog(self):
        """Mostra o diálogo de login"""
        dialog = LoginDialog(self.api_client, self)
        dialog.login_successful.connect(self.on_login_success)
        dialog.exec()
        
    def on_login_success(self, user_data):
        """Chamado quando o login é bem-sucedido"""
        self.current_user = user_data
        self.header.set_user_logged_in(user_data)
        
    def logout(self):
        """Realiza o logout"""
        self.current_user = None
        self.header.set_user_logged_out()
        
    def show_catalog(self):
        """Mostra a página do catálogo"""
        self.content_stack.setCurrentWidget(self.catalog_page)
        
    def show_my_tickets(self):
        """Mostra a página dos meus ingressos"""
        if self.current_user:
            self.content_stack.setCurrentWidget(self.my_tickets_page)
            self.my_tickets_page.load_user_tickets()
            
    def show_admin(self):
        """Mostra a página de administração"""
        if self.current_user and (self.current_user.get('is_superuser') or self.current_user.get('is_operator')):
            self.content_stack.setCurrentWidget(self.admin_page)
            self.admin_page.load_initial_data()
        

async def main():
    """Função principal assíncrona"""
    app = QApplication(sys.argv)
    
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = MainWindow()
    window.show()
    
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
