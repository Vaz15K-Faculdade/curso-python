"""
Componente de Card padronizado para a aplicação Toten Virtual
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from frontend.styles import COLORS, SIZES, FONTS


class Card(QFrame):
    """Componente de card padronizado"""
    
    clicked = Signal()
    
    def __init__(self, title=None, subtitle=None, content=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.setup_ui()
        self.setup_style()
        
    def setup_ui(self):
        """Configura a interface do card"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(SIZES['card_padding'], SIZES['card_padding'], 
                                           SIZES['card_padding'], SIZES['card_padding'])
        self.main_layout.setSpacing(SIZES['spacing_small'])
        
        # Título
        if self.title:
            self.title_label = QLabel(self.title)
            self.title_label.setObjectName("card_title")
            title_font = QFont()
            title_font.setPointSize(FONTS['size_medium'])
            title_font.setBold(True)
            self.title_label.setFont(title_font)
            self.main_layout.addWidget(self.title_label)
        
        # Subtítulo
        if self.subtitle:
            self.subtitle_label = QLabel(self.subtitle)
            self.subtitle_label.setObjectName("card_subtitle")
            self.subtitle_label.setWordWrap(True)
            self.main_layout.addWidget(self.subtitle_label)
        
        # Conteúdo
        if self.content:
            self.content_label = QLabel(self.content)
            self.content_label.setObjectName("card_content")
            self.content_label.setWordWrap(True)
            self.main_layout.addWidget(self.content_label)
            
    def setup_style(self):
        """Aplica o estilo do card"""
        self.setStyleSheet(f"""
            Card {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {SIZES['border_radius']}px;
                padding: 0;
                margin: 2px;
            }}
            
            Card:hover {{
                border-color: {COLORS['secondary']};
                background-color: {COLORS['surface_dark']};
            }}
            
            QLabel#card_title {{
                color: {COLORS['primary']};
                font-weight: 600;
                font-size: {FONTS['size_medium']}px;
            }}
            
            QLabel#card_subtitle {{
                color: {COLORS['text_light']};
                font-size: {FONTS['size_small']}px;
            }}
            
            QLabel#card_content {{
                color: {COLORS['text']};
                font-size: {FONTS['size_normal']}px;
            }}
        """)
        
    def mousePressEvent(self, event):
        """Captura clique no card"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
        
    def set_title(self, title):
        """Define o título do card"""
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)
            
    def set_subtitle(self, subtitle):
        """Define o subtítulo do card"""
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)
            
    def set_content(self, content):
        """Define o conteúdo do card"""
        if hasattr(self, 'content_label'):
            self.content_label.setText(content)
            
    def add_widget(self, widget):
        """Adiciona um widget ao card"""
        self.main_layout.addWidget(widget)


class ActionCard(Card):
    """Card com botões de ação"""
    
    def __init__(self, title=None, subtitle=None, content=None, action_list=None, parent=None):
        self.action_list = action_list or []
        super().__init__(title, subtitle, content, parent)
        self.add_actions()
        
    def add_actions(self):
        """Adiciona botões de ação ao card"""
        if self.action_list:
            # Layout para botões
            button_layout = QHBoxLayout()
            button_layout.setSpacing(SIZES['spacing_small'])
            
            for action in self.action_list:
                btn = QPushButton(action.get('text', 'Ação'))
                btn.setObjectName(f"action_btn_{action.get('type', 'primary')}")
                
                # Conecta o callback se fornecido
                if 'callback' in action:
                    btn.clicked.connect(action['callback'])
                    
                button_layout.addWidget(btn)
                
            # Adiciona espaçador se necessário
            button_layout.addStretch()
            
            self.main_layout.addLayout(button_layout)
            
        # Atualiza estilo para incluir botões
        self.update_action_style()
        
    def update_action_style(self):
        """Atualiza o estilo para incluir botões de ação"""
        current_style = self.styleSheet()
        action_style = f"""
            QPushButton#action_btn_primary {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-weight: 600;
                min-height: 24px;
            }}
            
            QPushButton#action_btn_primary:hover {{
                background-color: {COLORS['secondary_dark']};
            }}
            
            QPushButton#action_btn_secondary {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-weight: 600;
                min-height: 24px;
            }}
            
            QPushButton#action_btn_secondary:hover {{
                background-color: {COLORS['accent_dark']};
            }}
            
            QPushButton#action_btn_outline {{
                background-color: transparent;
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['border_radius_small']}px;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-weight: 600;
                min-height: 24px;
            }}
            
            QPushButton#action_btn_outline:hover {{
                background-color: {COLORS['surface_dark']};
                border-color: {COLORS['secondary']};
            }}
        """
        
        self.setStyleSheet(current_style + action_style)


class EventCard(ActionCard):
    """Card específico para eventos"""
    
    event_details_requested = Signal(dict)
    purchase_requested = Signal(dict)
    
    def __init__(self, event_data, parent=None):
        self.event_data = event_data
        
        # Prepara as ações do evento
        actions = [
            {
                'text': '👁️ Detalhes',
                'type': 'outline',
                'callback': self.show_details
            },
            {
                'text': '🎫 Comprar',
                'type': 'primary',
                'callback': self.request_purchase
            }
        ]
        
        super().__init__(
            title=event_data.get('name', 'Evento'),
            subtitle=f"📅 {event_data.get('data', '')} • 🕐 {event_data.get('hora', '')}",
            content=f"📍 {event_data.get('local', '')}",
            action_list=actions,
            parent=parent
        )
        
    def show_details(self):
        """Emite sinal para mostrar detalhes do evento"""
        self.event_details_requested.emit(self.event_data)
        
    def request_purchase(self):
        """Emite sinal para solicitar compra"""
        self.purchase_requested.emit(self.event_data)
