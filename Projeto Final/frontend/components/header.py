from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel, 
                               QPushButton, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from frontend.styles import get_header_stylesheet, SIZES, FONTS, COLORS


class HeaderWidget(QWidget):
    # Sinais
    login_requested = Signal()
    logout_requested = Signal()
    catalog_clicked = Signal()
    my_tickets_clicked = Signal()
    admin_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.setup_ui()
        self.setup_style()
        
    def setup_ui(self):
        """Configura a interface do cabeçalho"""
        self.setFixedHeight(SIZES['header_height'])
        
        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(SIZES['spacing_large'], SIZES['spacing_small'], 
                                     SIZES['spacing_large'], SIZES['spacing_small'])
        main_layout.setSpacing(SIZES['spacing'])
        
        # Logo da empresa (esquerda)
        self.logo_label = QLabel("TOTEN VIRTUAL")
        self.logo_label.setObjectName("logo")  # Para aplicar estilo específico
        logo_font = QFont()
        logo_font.setPointSize(FONTS['size_large'])
        logo_font.setBold(True)
        self.logo_label.setFont(logo_font)
        main_layout.addWidget(self.logo_label)
        
        # Espaçador
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        main_layout.addItem(spacer)
        
        # Menu de navegação (centro)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(SIZES['spacing'])
        
        self.catalog_btn = QPushButton("📚 Catálogo")
        self.catalog_btn.setFixedSize(110, SIZES['button_height'])
        self.catalog_btn.clicked.connect(self.catalog_clicked.emit)
        nav_layout.addWidget(self.catalog_btn)
        
        self.my_tickets_btn = QPushButton("🎫 Meus Ingressos")
        self.my_tickets_btn.setFixedSize(140, SIZES['button_height'])
        self.my_tickets_btn.clicked.connect(self.my_tickets_clicked.emit)
        self.my_tickets_btn.setEnabled(False)  # Desabilitado até fazer login
        nav_layout.addWidget(self.my_tickets_btn)
        
        # Botão de administração (só aparece para admins/operadores)
        self.admin_btn = QPushButton("🔧 Admin")
        self.admin_btn.setFixedSize(100, SIZES['button_height'])
        self.admin_btn.clicked.connect(self.admin_clicked.emit)
        self.admin_btn.setVisible(False)  # Oculto até login com permissões
        nav_layout.addWidget(self.admin_btn)
        
        main_layout.addLayout(nav_layout)
        
        # Espaçador
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        main_layout.addItem(spacer2)
        
        # Área do usuário (direita)
        user_layout = QHBoxLayout()
        user_layout.setSpacing(10)
        
        # Foto do usuário (placeholder)
        self.user_photo = QLabel()
        self.user_photo.setFixedSize(50, 50)
        self.user_photo.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {COLORS['border']};
                border-radius: 25px;
                background-color: {COLORS['surface_dark']};
                color: {COLORS['text_light']};
                font-size: {FONTS['size_large']}px;
            }}
        """)
        self.user_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_photo.setText("👤")
        self.user_photo.hide()  # Oculto até fazer login
        user_layout.addWidget(self.user_photo)
        
        # Nome do usuário
        self.user_name_label = QLabel()
        self.user_name_label.hide()  # Oculto até fazer login
        user_layout.addWidget(self.user_name_label)
        
        # Botão de login/logout
        self.auth_btn = QPushButton("🔐 Login")
        self.auth_btn.setFixedSize(90, SIZES['button_height'])
        self.auth_btn.clicked.connect(self.on_auth_button_clicked)
        user_layout.addWidget(self.auth_btn)
        
        main_layout.addLayout(user_layout)
        
    def setup_style(self):
        """Configura o estilo do cabeçalho"""
        self.setStyleSheet(get_header_stylesheet())
        
    def on_auth_button_clicked(self):
        """Manipula o clique no botão de autenticação"""
        if self.current_user is None:
            self.login_requested.emit()
        else:
            self.logout_requested.emit()
            
    def set_user_logged_in(self, user_data):
        """Define o usuário como logado"""
        self.current_user = user_data
        
        # Atualiza a interface
        self.user_name_label.setText(f"Olá, {user_data.get('email', 'Usuário')}")
        self.user_name_label.show()
        self.user_photo.show()
        
        self.auth_btn.setText("🚪 Logout")
        self.my_tickets_btn.setEnabled(True)
        
        # Mostra botão de admin se o usuário tem permissões
        if user_data.get('is_superuser') or user_data.get('is_operator'):
            self.admin_btn.setVisible(True)
        
    def set_user_logged_out(self):
        """Define o usuário como deslogado"""
        self.current_user = None
        
        # Atualiza a interface
        self.user_name_label.hide()
        self.user_photo.hide()
        
        self.auth_btn.setText("🔐 Login")
        self.my_tickets_btn.setEnabled(False)
        self.admin_btn.setVisible(False)
