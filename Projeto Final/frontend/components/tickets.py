from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame,
                               QMessageBox, QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
import asyncio
import base64
from collections import defaultdict
from frontend.styles import COLORS, SIZES, FONTS, get_button_stylesheet


class QRCodeDialog(QDialog):
    """Diálogo para exibir QR Code do ingresso"""
    
    def __init__(self, ticket, parent=None):
        super().__init__(parent)
        self.ticket = ticket
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("QR Code do Ingresso")
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel(f"Ingresso - {self.ticket['event']['name']}")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Informações do ingresso
        info_layout = QVBoxLayout()
        
        codigo_label = QLabel(f"Código: {self.ticket['codigo_ingresso']}")
        codigo_label.setFont(QFont("Arial", 10))
        codigo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(codigo_label)
        
        valor_label = QLabel(f"Valor: R$ {self.ticket['valor_pago']:.2f}")
        valor_label.setFont(QFont("Arial", 10))
        valor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(valor_label)
        
        layout.addLayout(info_layout)
        
        # QR Code
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_label.setMinimumHeight(250)
        
        if 'qr_code' in self.ticket and self.ticket['qr_code']:
            # Decodifica o QR code base64
            try:
                qr_data = base64.b64decode(self.ticket['qr_code'])
                pixmap = QPixmap()
                pixmap.loadFromData(qr_data)
                
                # Redimensiona mantendo proporção
                scaled_pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                qr_label.setPixmap(scaled_pixmap)
            except Exception as e:
                qr_label.setText(f"Erro ao carregar QR Code: {str(e)}")
                qr_label.setStyleSheet("color: red; font-size: 12px;")
        else:
            qr_label.setText("QR Code não disponível")
            qr_label.setStyleSheet("color: gray; font-size: 14px;")
        
        layout.addWidget(qr_label)
        
        # Botão fechar
        btn_fechar = QPushButton("Fechar")
        btn_fechar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['border']};
                color: {COLORS['text']};
                border: none;
                border-radius: {SIZES['border_radius']}px;
                font-weight: 600;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-size: {FONTS['size_normal']}px;
                min-height: {SIZES['button_height']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['border_light']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['disabled']};
            }}
        """)
        btn_fechar.clicked.connect(self.accept)
        layout.addWidget(btn_fechar)


class TicketGroupCard(QFrame):
    """Card para agrupar ingressos por evento"""
    
    def __init__(self, event_name, tickets_list):
        super().__init__()
        self.event_name = event_name
        self.tickets_list = tickets_list
        self.tickets_visible = False
        self.setup_ui()
        self.setup_style()
        
    def setup_ui(self):
        """Configura a interface do card agrupado"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Cabeçalho clicável
        header_layout = QHBoxLayout()
        
        # Nome do evento
        event_label = QLabel(self.event_name)
        event_label.setObjectName("event_name")
        event_font = QFont()
        event_font.setPointSize(FONTS['size_large'])
        event_font.setBold(True)
        event_label.setFont(event_font)
        header_layout.addWidget(event_label)
        
        # Quantidade de ingressos
        count_label = QLabel(f"{len(self.tickets_list)} ingresso(s)")
        count_label.setObjectName("count_label")
        count_label.setStyleSheet(f"color: {COLORS['text_light']}; font-weight: bold;")
        header_layout.addWidget(count_label)
        
        header_layout.addStretch()
        
        # Botão para expandir/recolher
        self.toggle_btn = QPushButton("Ver Ingressos")
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius']}px;
                font-weight: 600;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-size: {FONTS['size_normal']}px;
                min-height: {SIZES['button_height']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']}dd;
            }}
        """)
        self.toggle_btn.clicked.connect(self.toggle_tickets)
        header_layout.addWidget(self.toggle_btn)
        
        layout.addLayout(header_layout)
        
        # Informações do evento (primeira ocorrência)
        if self.tickets_list:
            first_ticket = self.tickets_list[0]
            event_info = first_ticket["event"]
            
            info_layout = QHBoxLayout()
            
            date_label = QLabel(f"📅 {event_info['data']} às {event_info['hora']}")
            info_layout.addWidget(date_label)
            
            location_label = QLabel(f"📍 {event_info['localizacao']}")
            info_layout.addWidget(location_label)
            
            info_layout.addStretch()
            layout.addLayout(info_layout)
        
        # Container para os ingressos (inicialmente oculto)
        self.tickets_container = QWidget()
        self.tickets_container.hide()
        
        tickets_layout = QVBoxLayout(self.tickets_container)
        tickets_layout.setContentsMargins(20, 10, 10, 10)
        tickets_layout.setSpacing(10)
        
        # Criar mini-cards para cada ingresso
        for i, ticket in enumerate(self.tickets_list):
            ticket_mini_card = self.create_mini_ticket_card(ticket, i + 1)
            tickets_layout.addWidget(ticket_mini_card)
            
        layout.addWidget(self.tickets_container)
        
    def create_mini_ticket_card(self, ticket, number):
        """Cria um mini-card para um ingresso individual"""
        mini_card = QFrame()
        mini_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface_dark']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {SIZES['border_radius_small']}px;
                padding: {SIZES['spacing_small']}px;
            }}
        """)
        
        layout = QHBoxLayout(mini_card)
        layout.setContentsMargins(SIZES['spacing'], SIZES['spacing_small'], SIZES['spacing'], SIZES['spacing_small'])
        
        # Número do ingresso
        number_label = QLabel(f"#{number}")
        number_label.setStyleSheet(f"font-weight: bold; color: {COLORS['primary']};")
        number_label.setFixedWidth(30)
        layout.addWidget(number_label)
        
        # Código do ingresso
        code_label = QLabel(f"Código: {ticket['codigo_ingresso']}")
        code_label.setStyleSheet(f"color: {COLORS['text_light']};")
        layout.addWidget(code_label)
        
        # Valor pago
        value_label = QLabel(f"R$ {ticket['valor_pago']:.2f}")
        value_label.setStyleSheet(f"font-weight: bold; color: {COLORS['success']};")
        layout.addWidget(value_label)
        
        # Status
        status_text = "Ativo" if ticket["status"] == "ativo" else ticket["status"].capitalize()
        status_label = QLabel(status_text)
        if ticket["status"] == "ativo":
            status_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
        else:
            status_label.setStyleSheet(f"color: {COLORS['text_light']}; font-weight: bold;")
        layout.addWidget(status_label)
        
        layout.addStretch()
        
        # Botão QR Code
        qr_btn = QPushButton("QR")
        qr_btn.setFixedSize(40, 25)
        qr_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                font-size: {FONTS['size_small']}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_dark']};
            }}
        """)
        qr_btn.clicked.connect(lambda: self.show_qr_code(ticket))
        layout.addWidget(qr_btn)
        
        return mini_card
        
    def toggle_tickets(self):
        """Alterna a visibilidade dos ingressos"""
        if self.tickets_visible:
            self.tickets_container.hide()
            self.toggle_btn.setText("Ver Ingressos")
            self.tickets_visible = False
        else:
            self.tickets_container.show()
            self.toggle_btn.setText("Ocultar")
            self.tickets_visible = True
            
    def show_qr_code(self, ticket):
        """Mostra o QR Code do ingresso"""
        dialog = QRCodeDialog(ticket, self)
        dialog.exec()
        
    def setup_style(self):
        """Configura o estilo do card usando o sistema padronizado"""
        button_style = get_button_stylesheet('primary')
        
        self.setStyleSheet(f"""
            TicketGroupCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {SIZES['border_radius']}px;
                margin: {SIZES['spacing_small']}px;
            }}
            
            TicketGroupCard:hover {{
                border-color: {COLORS['secondary']};
                background-color: {COLORS['surface_dark']};
            }}
            
            QLabel {{
                color: {COLORS['text']};
                font-size: {FONTS['size_normal']}px;
            }}
            
            QLabel#event_name {{
                color: {COLORS['primary']};
                font-weight: 600;
                font-size: {FONTS['size_large']}px;
            }}
            
            QLabel#count_label {{
                color: {COLORS['text_light']};
                font-weight: bold;
            }}
            
            {button_style}
        """)


class TicketCard(QFrame):
    """Card individual para exibir um ingresso"""
    
    def __init__(self, ticket_data):
        super().__init__()
        self.ticket_data = ticket_data
        self.setup_ui()
        self.setup_style()
        
    def setup_ui(self):
        """Configura a interface do card"""
        self.setFixedSize(350, 180)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Cabeçalho com nome do evento
        header_layout = QHBoxLayout()
        
        event_label = QLabel(self.ticket_data["event"]["name"])
        event_font = QFont()
        event_font.setPointSize(14)
        event_font.setBold(True)
        event_label.setFont(event_font)
        event_label.setWordWrap(True)
        header_layout.addWidget(event_label)
        
        # Status do ingresso
        status_label = QLabel(self.ticket_data["status"])
        status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_font = QFont()
        status_font.setBold(True)
        status_label.setFont(status_font)
        
        status_text = "Ativo" if self.ticket_data["status"] == "ativo" else self.ticket_data["status"].capitalize()
        status_label.setText(status_text)

        if self.ticket_data["status"] == "ativo":
            status_label.setStyleSheet("color: #27ae60;")
        else:
            status_label.setStyleSheet("color: #e74c3c;")
            
        header_layout.addWidget(status_label)
        layout.addLayout(header_layout)
        
        # Data e hora do evento
        datetime_label = QLabel(f"📅 {self.ticket_data['event']['data']} às {self.ticket_data['event']['hora']}")
        layout.addWidget(datetime_label)
        
        # Local
        location_label = QLabel(f"📍 {self.ticket_data['event']['localizacao']}")
        layout.addWidget(location_label)
        
        # Assento (se disponível)
        if self.ticket_data.get("numero_assento"):
            seat_label = QLabel(f"🎫 Assento: {self.ticket_data['numero_assento']}")
            layout.addWidget(seat_label)
            
        # Data da compra
        purchase_label = QLabel(f"Comprado em: {self.ticket_data['data_compra']}")
        purchase_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(purchase_label)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        view_btn = QPushButton("Ver Detalhes")
        view_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius']}px;
                font-weight: 600;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-size: {FONTS['size_normal']}px;
                min-height: {SIZES['button_height']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']}dd;
            }}
        """)
        view_btn.clicked.connect(self.view_details)
        buttons_layout.addWidget(view_btn)
        
        if self.ticket_data["status"] == "ativo":
            qr_btn = QPushButton("QR Code")
            qr_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    color: {COLORS['text_white']};
                    border: none;
                    border-radius: {SIZES['border_radius']}px;
                    font-weight: 600;
                    padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                    font-size: {FONTS['size_normal']}px;
                    min-height: {SIZES['button_height']}px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['accent_dark']};
                }}
            """)
            qr_btn.clicked.connect(self.show_qr_code)
            buttons_layout.addWidget(qr_btn)
            
        layout.addLayout(buttons_layout)
        
    def setup_style(self):
        """Configura o estilo do card usando o sistema padronizado"""
        button_style = get_button_stylesheet('primary')
        
        self.setStyleSheet(f"""
            TicketCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {SIZES['border_radius']}px;
                border-left: 4px solid {COLORS['secondary']};
                padding: 0;
                margin: 2px;
            }}
            
            TicketCard:hover {{
                border-color: {COLORS['secondary']};
                background-color: {COLORS['surface_dark']};
            }}
            
            QLabel {{
                color: {COLORS['text']};
                font-size: {FONTS['size_normal']}px;
            }}
            
            QLabel#ticket_title {{
                color: {COLORS['primary']};
                font-weight: 600;
                font-size: {FONTS['size_medium']}px;
            }}
            
            QLabel#ticket_subtitle {{
                color: {COLORS['text_light']};
                font-size: {FONTS['size_small']}px;
            }}
            
            {button_style}
        """)
        
    def view_details(self):
        """Mostra os detalhes do ingresso"""
        details = f"""
        Evento: {self.ticket_data['event']['name']}
        Data: {self.ticket_data['event']['data']} às {self.ticket_data['event']['hora']}
        Local: {self.ticket_data['event']['localizacao']}
        """
        
        if self.ticket_data.get("numero_assento"):
            details += f"\nAssento: {self.ticket_data['numero_assento']}"
            
        status_text = "Ativo" if self.ticket_data["status"] == "ativo" else self.ticket_data["status"].capitalize()
        details += f"""
        Status: {status_text}
        Comprado em: {self.ticket_data['data_compra']}
        """
        
        QMessageBox.information(self, "Detalhes do Ingresso", details)
        
    def show_qr_code(self):
        """Mostra o QR Code do ingresso"""
        dialog = QRCodeDialog(self.ticket_data, self)
        dialog.exec()


class MyTicketsWidget(QWidget):
    """Widget principal para exibir os ingressos do usuário"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.tickets = []
        self.current_user_id = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface dos ingressos"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Cabeçalho da página
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Meus Ingressos")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        # Botão de atualizar
        update_btn = QPushButton("🔄 Recarregar")
        update_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                font-weight: 600;
                padding: 4px 8px;
                font-size: {FONTS['size_small']}px;
                min-height: 28px;
                max-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_dark']};
            }}
        """)
        update_btn.clicked.connect(self.refresh_tickets)
        header_layout.addWidget(update_btn)
        
        layout.addLayout(header_layout)
        
        # Área de rolagem para os ingressos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget do conteúdo dos ingressos
        self.tickets_widget = QWidget()
        self.tickets_layout = QVBoxLayout(self.tickets_widget)  # Mudança para VBoxLayout
        self.tickets_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tickets_layout.setSpacing(15)
        
        scroll_area.setWidget(self.tickets_widget)
        layout.addWidget(scroll_area)
        
        # Mensagem quando não há ingressos
        self.no_tickets_label = QLabel("Você ainda não possui ingressos.\nVisite o catálogo para comprar!")
        self.no_tickets_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_tickets_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 16px;
                padding: 40px;
            }
        """)
        self.no_tickets_label.hide()
        layout.addWidget(self.no_tickets_label)
        
        # Mensagem de carregamento
        self.loading_label = QLabel("Carregando ingressos...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
    def load_user_tickets(self):
        """Carrega os ingressos do usuário"""
        self.loading_label.show()
        self.no_tickets_label.hide()
        self.clear_tickets()
        asyncio.create_task(self._async_load_tickets())
        
    def refresh_tickets(self):
        """Atualiza os ingressos"""
        self.load_user_tickets()
            
    async def _async_load_tickets(self):
        """Carrega os ingressos de forma assíncrona"""
        try:
            # Usa o cliente da API injetado
            result = await self.api_client.get_meus_ingressos()
            
            if result["success"]:
                self.tickets = result["tickets"]
                self.display_tickets()
            else:
                # Verifica se é erro de conexão com a API
                error_msg = result['error']
                if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg or "Conexão recusada" in error_msg:
                    QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                else:
                    QMessageBox.critical(self, "Erro", f"Erro ao carregar ingressos: {error_msg}")
        except Exception as e:
            error_str = str(e)
            if "Max retries exceeded" in error_str or "Failed to establish a new connection" in error_str or "Conexão recusada" in error_str:
                QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
            else:
                QMessageBox.critical(self, "Erro", f"Erro inesperado: {error_str}")
        finally:
            self.loading_label.hide()
            
    def display_tickets(self):
        """Exibe os ingressos agrupados por evento"""
        if not self.tickets:
            self.no_tickets_label.show()
            return
            
        # Agrupar ingressos por evento
        eventos_agrupados = defaultdict(list)
        for ticket in self.tickets:
            event_name = ticket["event"]["name"]
            eventos_agrupados[event_name].append(ticket)
        
        # Criar cards agrupados para cada evento
        for event_name, tickets_list in eventos_agrupados.items():
            group_card = TicketGroupCard(event_name, tickets_list)
            self.tickets_layout.addWidget(group_card)
                
    def clear_tickets(self):
        """Remove todos os ingressos da grade"""
        while self.tickets_layout.count():
            child = self.tickets_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
