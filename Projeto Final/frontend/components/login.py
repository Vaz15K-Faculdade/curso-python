from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTabWidget, QWidget, 
                               QFormLayout, QMessageBox, QDateEdit, QFrame)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont
from frontend.styles import get_dialog_stylesheet, get_button_stylesheet, get_input_stylesheet, COLORS, SIZES, FONTS
import asyncio
import re
from validate_docbr import CPF


class LoginDialog(QDialog):
    login_successful = Signal(dict)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
        self.setup_style()
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        self.setWindowTitle("Login / Cadastro")
        self.setFixedSize(450, 550)
        self.setModal(True)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("Bem-vindo ao Toten Virtual")
        title_label.setObjectName("title")
        title_font = QFont()
        title_font.setPointSize(FONTS['size_title'])
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Abas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Aba de Login
        self.login_tab = self.create_login_tab()
        self.tab_widget.addTab(self.login_tab, "Login")
        
        # Aba de Cadastro
        self.register_tab = self.create_register_tab()
        self.tab_widget.addTab(self.register_tab, "Cadastro")
        
    def create_login_tab(self):
        """Cria a aba de login"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Formulário de login
        form_layout = QFormLayout()
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("seu@email.com")
        form_layout.addRow("Email:", self.login_email)
        
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Sua senha")
        form_layout.addRow("Senha:", self.login_password)
        
        layout.addLayout(form_layout)
        
        # Botão de login
        self.login_btn = QPushButton("Entrar")
        self.login_btn.setFixedHeight(40)
        self.login_btn.clicked.connect(self.perform_login)
        layout.addWidget(self.login_btn)
        
        # Conectar Enter para fazer login
        self.login_password.returnPressed.connect(self.perform_login)
        
        return tab
        
    def create_register_tab(self):
        """Cria a aba de cadastro"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Formulário de cadastro
        form_layout = QFormLayout()
        
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("seu@email.com")
        form_layout.addRow("Email:", self.register_email)
        
        self.register_cpf = QLineEdit()
        self.register_cpf.setPlaceholderText("000.000.000-00")
        form_layout.addRow("CPF:", self.register_cpf)
        
        self.register_phone = QLineEdit()
        self.register_phone.setPlaceholderText("(11) 99999-9999")
        form_layout.addRow("Telefone:", self.register_phone)
        
        self.register_birth_date = QDateEdit()
        self.register_birth_date.setDate(QDate(2000, 1, 1))
        self.register_birth_date.setCalendarPopup(True)
        form_layout.addRow("Data de Nascimento:", self.register_birth_date)
        
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password.setPlaceholderText("Sua senha")
        form_layout.addRow("Senha:", self.register_password)
        
        self.register_password_confirm = QLineEdit()
        self.register_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_confirm.setPlaceholderText("Confirme sua senha")
        form_layout.addRow("Confirmar Senha:", self.register_password_confirm)
        
        layout.addLayout(form_layout)
        
        # Botão de cadastro
        self.register_btn = QPushButton("Cadastrar")
        self.register_btn.setFixedHeight(40)
        self.register_btn.clicked.connect(self.perform_register)
        layout.addWidget(self.register_btn)
        
        return tab
        
    def setup_style(self):
        """Configura o estilo do diálogo"""
        dialog_style = get_dialog_stylesheet()
        input_style = get_input_stylesheet()
        button_style = get_button_stylesheet('primary')
        
        self.setStyleSheet(f"""
            {dialog_style}
            {input_style}
            {button_style}
            
            QTabWidget::pane {{
                border: 1px solid {COLORS['border']};
                background-color: {COLORS['surface']};
                border-radius: {SIZES['border_radius_small']}px;
            }}
            
            QTabBar::tab {{
                background-color: {COLORS['border']};
                padding: {SIZES['spacing']}px {SIZES['spacing_large']}px;
                margin-right: 2px;
                border-top-left-radius: {SIZES['border_radius_small']}px;
                border-top-right-radius: {SIZES['border_radius_small']}px;
                color: {COLORS['text']};
                font-weight: 600;
            }}
            
            QTabBar::tab:selected {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_white']};
            }}
            
            QTabBar::tab:hover {{
                background-color: {COLORS['secondary_dark']};
                color: {COLORS['text_white']};
            }}
        """)
        
    def validate_email(self, email):
        """Valida o formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def validate_cpf(self, cpf):
        """Validação completa do CPF usando biblioteca validate-docbr"""
        cpf_validator = CPF()
        # Remove caracteres não numéricos
        cpf_numbers = re.sub(r'[^0-9]', '', cpf)
        return cpf_validator.validate(cpf_numbers)
        
    def perform_login(self):
        """Executa o login"""
        email = self.login_email.text().strip()
        password = self.login_password.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return
            
        if not self.validate_email(email):
            QMessageBox.warning(self, "Erro", "Por favor, digite um email válido.")
            return
            
        # Desabilita o botão durante o processo
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Entrando...")
        
        # Executa o login de forma assíncrona
        asyncio.create_task(self._async_login(email, password))
        
    async def _async_login(self, email, password):
        """Executa o login de forma assíncrona"""
        try:
            result = await self.api_client.login(email, password)
            
            if result["success"]:
                self.login_successful.emit(result["user"])
                self.accept()
            else:
                QMessageBox.critical(self, "Erro de Login", result["error"])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Entrar")
            
    def perform_register(self):
        """Executa o cadastro"""
        email = self.register_email.text().strip()
        cpf = self.register_cpf.text().strip()
        phone = self.register_phone.text().strip()
        birth_date_qdate = self.register_birth_date.date()
        birth_date = f"{birth_date_qdate.year()}-{birth_date_qdate.month():02d}-{birth_date_qdate.day():02d}"
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()
        
        # Validações
        if not all([email, cpf, phone, password, password_confirm]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return
            
        if not self.validate_email(email):
            QMessageBox.warning(self, "Erro", "Por favor, digite um email válido.")
            return
            
        if not self.validate_cpf(cpf):
            QMessageBox.warning(self, "Erro", "Por favor, digite um CPF válido.")
            return
            
        if password != password_confirm:
            QMessageBox.warning(self, "Erro", "As senhas não conferem.")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres.")
            return
            
        # Desabilita o botão durante o processo
        self.register_btn.setEnabled(False)
        self.register_btn.setText("Cadastrando...")
        
        # Dados do usuário
        user_data = {
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "is_operator": False,
            "is_verified": False,
            "cpf": cpf,
            "telefone": phone,
            "data_nascimento": birth_date
        }
        
        # Executa o cadastro de forma assíncrona
        asyncio.create_task(self._async_register(user_data))
        
    async def _async_register(self, user_data):
        """Executa o cadastro de forma assíncrona"""
        try:
            result = await self.api_client.registrar_usuario(user_data)
            
            if result["success"]:
                QMessageBox.information(
                    self, 
                    "Cadastro Realizado", 
                    "Cadastro realizado com sucesso! Você pode fazer login agora."
                )
                # Muda para a aba de login
                self.tab_widget.setCurrentIndex(0)
                # Preenche o email no login
                self.login_email.setText(user_data["email"])
            else:
                QMessageBox.critical(self, "Erro de Cadastro", result["error"])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
        finally:
            self.register_btn.setEnabled(True)
            self.register_btn.setText("Cadastrar")
