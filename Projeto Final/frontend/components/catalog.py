from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame, QGridLayout,
                               QMessageBox, QSizePolicy, QDialog, QGroupBox,
                               QTextEdit)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from frontend.styles import (get_button_stylesheet, get_dialog_stylesheet, 
                   COLORS, SIZES, FONTS)
import asyncio


class EventDetailsDialog(QDialog):
    """Diálogo para exibir detalhes completos do evento"""
    
    def __init__(self, dados_evento, api_client, parent=None):
        super().__init__(parent)
        self.dados_evento = dados_evento
        self.api_client = api_client
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        self.setWindowTitle(f"Detalhes - {self.dados_evento['name']}")
        self.setFixedSize(750, 650)  # Aumentado para acomodar melhor o conteúdo
        self.setModal(True)
        
        # Aplica estilos padronizados
        dialog_style = get_dialog_stylesheet()
        button_style = get_button_stylesheet('primary')
        
        self.setStyleSheet(f"""
            {dialog_style}
            {button_style}
            
            QGroupBox {{
                font-weight: 600;
                font-size: {FONTS['size_medium']}px;
                color: {COLORS['primary']};
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['border_radius']}px;
                margin-top: {SIZES['spacing']}px;
                padding-top: {SIZES['spacing']}px;
                background-color: {COLORS['surface']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 5px 10px;
                background-color: {COLORS['secondary']};
                color: {COLORS['text_white']};
                border-radius: {SIZES['border_radius_small']}px;
            }}
            
            QLabel {{
                color: {COLORS['text']};
                font-size: {FONTS['size_normal']}px;
            }}
            
            QLabel#title {{
                color: {COLORS['primary']};
                font-size: {FONTS['size_title']}px;
                font-weight: 700;
            }}
        """)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: {COLORS['border_light']};
                border: none;
                border-radius: 6px;
                width: 12px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['border']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {COLORS['text_light']};
            }}
        """)
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)  # Reduzido
        layout.setSpacing(15)  # Reduzido
        
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['secondary']}, stop:1 {COLORS['secondary_dark']});
                border-radius: {SIZES['border_radius']}px;
                padding: {SIZES['spacing']}px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        title_label = QLabel(self.dados_evento["name"])
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_white']};
                font-size: {FONTS['size_xlarge']}px;
                font-weight: 700;
                margin: 0;
                padding: 5px;
            }}
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)
        
        datetime_label = QLabel(f"📅 {self.dados_evento['data']} • 🕐 {self.dados_evento['hora']}")
        datetime_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_white']};
                font-size: {FONTS['size_small']}px;
                font-weight: 500;
                margin: 0;
                padding: 3px;
                opacity: 0.9;
            }}
        """)
        datetime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(datetime_label)
        
        layout.addWidget(header_frame)
        
        info_group = QGroupBox("ℹ️ Informações do Evento")
        info_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['border_radius_small']}px;
                margin-top: {SIZES['spacing_small']}px;
                padding: {SIZES['spacing_small']}px;
                color: {COLORS['primary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 8px 2px 8px;
            }}
        """)
        # Define política de tamanho para ajustar ao conteúdo
        info_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
        info_layout = QVBoxLayout(info_group)
        info_layout.setSpacing(6)
        info_layout.setContentsMargins(10, 8, 10, 8)
        
        # Estilo para labels de informação (mais compacto)
        info_style = f"""
            QLabel {{
                font-size: {FONTS['size_normal']}px;
                color: {COLORS['text']};
                padding: {SIZES['spacing_small']}px;
                margin: 1px;
                border-radius: {SIZES['border_radius_small']}px;
                background-color: {COLORS['surface_dark']};
                border: 1px solid {COLORS['border_light']};
                min-height: 30px;
            }}
        """
        
        local_row = QHBoxLayout()
        local_label_title = QLabel("📍 Local:")
        local_label_title.setFixedWidth(100)  # Largura fixa para alinhamento
        local_row.addWidget(local_label_title)
        local_label = QLabel(self.dados_evento['localizacao'])
        local_label.setStyleSheet(info_style)
        local_label.setWordWrap(True)  # Permitir quebra de linha
        local_label.setMinimumHeight(30)  # Altura mínima adequada
        local_row.addWidget(local_label, 1)  # Stretch factor 1 para ocupar espaço
        info_layout.addLayout(local_row)
        
        if 'categoria' in self.dados_evento:
            categoria_row = QHBoxLayout()
            categoria_label_title = QLabel("🏷️ Categoria:")
            categoria_label_title.setFixedWidth(100)
            categoria_row.addWidget(categoria_label_title)
            categoria_label = QLabel(self.dados_evento['categoria'])
            categoria_label.setStyleSheet(info_style)
            categoria_label.setWordWrap(True)
            categoria_label.setMinimumHeight(30)
            categoria_row.addWidget(categoria_label, 1)
            info_layout.addLayout(categoria_row)
        
        if 'organizador' in self.dados_evento:
            organizador_row = QHBoxLayout()
            organizador_label_title = QLabel("👤 Organizador:")
            organizador_label_title.setFixedWidth(100)
            organizador_row.addWidget(organizador_label_title)
            organizador_label = QLabel(self.dados_evento['organizador'])
            organizador_label.setStyleSheet(info_style)
            organizador_label.setWordWrap(True)
            organizador_label.setMinimumHeight(30)
            organizador_row.addWidget(organizador_label, 1)
            info_layout.addLayout(organizador_row)
        
        layout.addWidget(info_group, 0)  # Stretch factor 0 - tamanho mínimo
        
        desc_group = QGroupBox("📝 Descrição do Evento")
        desc_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 8px;
                padding: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 8px 2px 8px;
            }
        """)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setSpacing(6)
        desc_layout.setContentsMargins(10, 8, 10, 8)
        
        # Usar QTextEdit somente leitura para exibir descrições longas
        desc_text = QTextEdit()
        desc_text.setReadOnly(True)
        desc_text.setPlainText(self.dados_evento.get("description", "") or "")
        # Ajustes visuais semelhantes ao QLabel anterior
        desc_text.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {COLORS['border_light']};
                border-radius: {SIZES['border_radius_small']}px;
                background-color: {COLORS['surface']};
                padding: {SIZES['card_padding']}px;
                font-size: {FONTS['size_normal']}px;
                color: {COLORS['text']};
                margin: 2px;
            }}
        """)
        desc_text.setMinimumHeight(120)
        desc_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Remover borda extra do QFrame para que o visual fique plano
        desc_text.setFrameStyle(QFrame.Shape.NoFrame)
        # Garantir quebra de linha por palavra e ajuste à largura do widget
        desc_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        desc_layout.addWidget(desc_text)
        
        layout.addWidget(desc_group, 1)  # Stretch factor 1 - pode expandir
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(SIZES['spacing_small'])
        
        btn_comprar = QPushButton("Comprar Ingressos")
        btn_comprar.setFixedHeight(SIZES['button_height'])
        btn_comprar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius']}px;
                font-weight: 600;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-size: {FONTS['size_normal']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['success']}dd;
            }}
            QPushButton:pressed {{
                background-color: {COLORS['success']}bb;
            }}
        """)
        btn_comprar.clicked.connect(self.comprar_ingresso)
        buttons_layout.addWidget(btn_comprar)
        
        btn_fechar = QPushButton("Fechar")
        btn_fechar.setFixedHeight(SIZES['button_height'])
        btn_fechar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['border']};
                color: {COLORS['text']};
                border: none;
                border-radius: {SIZES['border_radius']}px;
                font-weight: 600;
                padding: {SIZES['spacing_small']}px {SIZES['spacing']}px;
                font-size: {FONTS['size_normal']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['border_light']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['disabled']};
            }}
        """)
        btn_fechar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_fechar)
        
        layout.addLayout(buttons_layout)
        
        scroll.setWidget(content_widget)
        
        # Layout principal do diálogo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def comprar_ingresso(self):
        """Abre o diálogo de compra de ingressos"""
        self.accept()  # Fecha este diálogo
        dialog = TicketPurchaseDialog(self.dados_evento, self.api_client, self.parent())
        dialog.exec()


class LoteWidget(QFrame):
    """Widget personalizado para representar um lote com seus controles"""
    def __init__(self, lote_data, parent_dialog=None):
        super().__init__()
        self.lote_data = lote_data
        self.lote_id = lote_data["id"]
        self.preco_unitario = float(lote_data["price"])
        self.max_disponivel = lote_data["ingressos_disponiveis"]
        self.quantidade_atual = 0
        self.parent_dialog = parent_dialog
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do widget do lote"""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(140)  # Aumentado para evitar corte
        self.setStyleSheet("""
            LoteWidget {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #fff;
                margin: 5px;
                padding: 10px;
            }
            LoteWidget:hover {
                border-color: #007bff;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)  # Aumentado espaçamento
        
        # Cabeçalho com informações do lote
        header_layout = QHBoxLayout()
        
        # Informações do lote
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)  # Espaçamento entre elementos
        
        # Nome do lote
        self.label_nome = QLabel(str(self.lote_data["name"]))
        self.label_nome.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 15px; 
                color: #333;
                margin: 0;
                padding: 3px 0;
                min-height: 20px;
            }
        """)
        self.label_nome.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        info_layout.addWidget(self.label_nome)
        
        # Preço e disponibilidade
        info_preco = QLabel(f"R$ {self.preco_unitario:.2f} por ingresso")
        info_preco.setStyleSheet("""
            QLabel {
                color: #27ae60; 
                font-weight: bold; 
                font-size: 13px;
                margin: 0;
                padding: 2px 0;
                min-height: 18px;
            }
        """)
        info_preco.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        info_layout.addWidget(info_preco)
        
        info_disponivel = QLabel(f"{self.max_disponivel} disponíveis")
        info_disponivel.setStyleSheet("""
            QLabel {
                color: #666; 
                font-size: 12px;
                margin: 0;
                padding: 2px 0;
                min-height: 16px;
            }
        """)
        info_disponivel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        info_layout.addWidget(info_disponivel)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        # Controles de quantidade
        controles_layout = QHBoxLayout()
        controles_layout.setSpacing(20)
        controles_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Botão diminuir
        self.btn_menos = QPushButton("−")
        self.btn_menos.setFixedSize(40, 40)
        self.btn_menos.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.btn_menos.setEnabled(False)
        self.btn_menos.clicked.connect(self.diminuir_quantidade)
        
        # Label quantidade - com altura fixa para evitar corte
        self.label_quantidade = QLabel("0")
        self.label_quantidade.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_quantidade.setFixedSize(70, 40)  # Aumentado largura
        self.label_quantidade.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 18px; 
                color: #333; 
                border: 2px solid #ddd; 
                border-radius: 8px; 
                background-color: #f8f9fa;
                padding: 0px;
                line-height: 40px;
            }
        """)
        
        # Botão aumentar
        self.btn_mais = QPushButton("+")
        self.btn_mais.setFixedSize(40, 40)
        self.btn_mais.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.btn_mais.clicked.connect(self.aumentar_quantidade)
        
        controles_layout.addWidget(self.btn_menos)
        controles_layout.addWidget(self.label_quantidade)
        controles_layout.addWidget(self.btn_mais)
        
        header_layout.addLayout(controles_layout)
        
        layout.addLayout(header_layout)
        
    def aumentar_quantidade(self):
        """Aumenta a quantidade de ingressos"""
        if self.quantidade_atual < self.max_disponivel and self.quantidade_atual < 10:
            self.quantidade_atual += 1
            self.label_quantidade.setText(str(self.quantidade_atual))
            
            # Atualiza botões
            self.btn_menos.setEnabled(self.quantidade_atual > 0)
            self.btn_mais.setEnabled(self.quantidade_atual < self.max_disponivel and self.quantidade_atual < 10)
            
            # Emite sinal para atualizar resumo
            if self.parent_dialog and hasattr(self.parent_dialog, 'atualizar_resumo'):
                self.parent_dialog.atualizar_resumo()
                
    def diminuir_quantidade(self):
        """Diminui a quantidade de ingressos"""
        if self.quantidade_atual > 0:
            self.quantidade_atual -= 1
            self.label_quantidade.setText(str(self.quantidade_atual))
            
            # Atualiza botões
            self.btn_menos.setEnabled(self.quantidade_atual > 0)
            self.btn_mais.setEnabled(True)
            
            # Emite sinal para atualizar resumo
            if self.parent_dialog and hasattr(self.parent_dialog, 'atualizar_resumo'):
                self.parent_dialog.atualizar_resumo()
                
    def get_quantidade(self):
        """Retorna a quantidade atual selecionada"""
        return self.quantidade_atual
        
    def get_valor_total(self):
        """Retorna o valor total para este lote"""
        return self.quantidade_atual * self.preco_unitario


class TicketPurchaseDialog(QDialog):
    """Diálogo para compra de ingressos com interface intuitiva"""
    
    def __init__(self, dados_evento, api_client, parent=None):
        super().__init__(parent)
        self.dados_evento = dados_evento
        self.api_client = api_client
        self.lotes = []
        self.lotes_widgets = []  # Lista para armazenar widgets dos lotes
        self.setup_ui()
        # Carregar lotes após configurar a UI
        QTimer.singleShot(100, lambda: asyncio.create_task(self.carregar_lotes()))
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        self.setWindowTitle(f"Comprar Ingressos - {self.dados_evento.get('name', 'Evento')}")
        self.setFixedSize(650, 600)
        self.setModal(True)
        
        # Estilo geral melhorado
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #333;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 10px 20px;
                background: #007bff;
                color: white;
                border-radius: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QLabel {
                color: #495057;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Área de lotes com design melhorado
        lotes_group = QGroupBox("Escolha seus Ingressos")
        lotes_group.setMinimumHeight(280)
        lotes_layout = QVBoxLayout(lotes_group)
        lotes_layout.setSpacing(15)
        lotes_layout.setContentsMargins(20, 25, 20, 20)
        
        # Label de carregamento estilizada
        self.label_carregando = QLabel("⏳ Carregando lotes disponíveis...")
        self.label_carregando.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 2px dashed #ffc107;
                border-radius: 8px;
                padding: 20px;
                font-size: 14px;
                color: #856404;
                font-weight: bold;
                text-align: center;
            }
        """)
        self.label_carregando.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lotes_layout.addWidget(self.label_carregando)
        
        # Scroll area para os lotes - melhorada
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)  # Reduzido para evitar sobreposição
        scroll_area.setMaximumHeight(250)  # Limitado altura máxima
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background: #ffffff;
            }
            QScrollBar:vertical {
                background: #f8f9fa;
                border: none;
                border-radius: 6px;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #6c757d;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #495057;
            }
        """)
        
        self.widget_lotes = QWidget()
        self.widget_lotes.setStyleSheet("background-color: #ffffff;")
        self.layout_lotes = QVBoxLayout(self.widget_lotes)
        self.layout_lotes.setSpacing(10)  # Reduzido espaçamento
        self.layout_lotes.setContentsMargins(10, 10, 10, 10)  # Reduzido margens
        
        scroll_area.setWidget(self.widget_lotes)
        lotes_layout.addWidget(scroll_area)
        
        layout.addWidget(lotes_group)
        
        # Resumo da compra melhorado
        resumo_group = QGroupBox("Resumo da Compra")
        resumo_group.setMaximumHeight(120)  # Limitado altura
        resumo_layout = QHBoxLayout(resumo_group)
        resumo_layout.setSpacing(20)
        resumo_layout.setContentsMargins(15, 20, 15, 15)  # Reduzido margens
        
        # Total de ingressos
        ingressos_container = QVBoxLayout()
        ingressos_container.setSpacing(5)
        
        ingressos_label = QLabel("Ingressos:")
        ingressos_label.setStyleSheet("font-size: 11px; color: #6c757d; margin-bottom: 2px;")
        
        self.label_total_ingressos = QLabel("0")
        self.label_total_ingressos.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #007bff;
                padding: 6px 10px;
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                text-align: center;
                min-height: 20px;
            }
        """)
        self.label_total_ingressos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ingressos_container.addWidget(ingressos_label)
        ingressos_container.addWidget(self.label_total_ingressos)
        resumo_layout.addLayout(ingressos_container)
        
        # Espaçador
        resumo_layout.addStretch()
        
        # Valor total
        total_container = QVBoxLayout()
        total_container.setSpacing(5)
        
        total_label = QLabel("Total:")
        total_label.setStyleSheet("font-size: 11px; color: #6c757d; margin-bottom: 2px;")
        
        self.label_valor_total = QLabel("R$ 0,00")
        self.label_valor_total.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #28a745;
                padding: 6px 10px;
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                text-align: center;
                min-height: 20px;
            }
        """)
        self.label_valor_total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        total_container.addWidget(total_label)
        total_container.addWidget(self.label_valor_total)
        resumo_layout.addLayout(total_container)
        layout.addWidget(resumo_group)
        
        # Botões melhorados
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 5, 0, 0)  # Reduzido margem superior
        
        # Botão comprar (lado esquerdo)
        self.botao_comprar = QPushButton("Comprar Ingressos")
        self.botao_comprar.setMinimumHeight(40)  # Reduzido altura
        self.botao_comprar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                min-width: 140px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1eb884);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #ffffff;
            }
        """)
        self.botao_comprar.clicked.connect(self.confirmar_compra)
        self.botao_comprar.setEnabled(False)
        buttons_layout.addWidget(self.botao_comprar)
        
        # Espaço entre os botões
        buttons_layout.addStretch()
        
        # Botão cancelar (lado direito)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setMinimumHeight(40)  # Reduzido altura
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        btn_cancelar.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancelar)
        
        layout.addLayout(buttons_layout)
        
    async def carregar_lotes(self):
        """Carrega os lotes disponíveis para o evento"""
        try:
            resultado = await self.api_client.get_lotes_evento(self.dados_evento["id"])
            
            if resultado["success"]:
                self.lotes = resultado["batches"]
                self.criar_widgets_lotes()
            else:
                # Verifica se é erro de conexão com a API
                error_msg = resultado['error']
                if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg or "Conexão recusada" in error_msg:
                    QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                    self.reject()
                else:
                    QMessageBox.critical(self, "Erro", f"Erro ao carregar lotes: {error_msg}")
                    self.reject()
                
        except Exception as e:
            error_str = str(e)
            if "Max retries exceeded" in error_str or "Failed to establish a new connection" in error_str or "Conexão recusada" in error_str:
                QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                self.reject()
            else:
                QMessageBox.critical(self, "Erro", f"Erro inesperado: {error_str}")
                self.reject()
            
    def criar_widgets_lotes(self):
        """Cria os widgets para cada lote disponível"""
        # Remove label de carregamento
        self.label_carregando.hide()
        
        # Filtra apenas lotes ativos disponíveis para venda
        # Observação: o backend usa status em inglês ("active"), mas algumas partes do
        # frontend usam "ativo"; aceitar ambos para compatibilidade.
        lotes_disponiveis = [
            lote for lote in self.lotes
            if lote.get("is_active") and lote.get("ingressos_disponiveis", 0) > 0
            and (lote.get("status") in ("active", "ativo"))
        ]
        
        if not lotes_disponiveis:
            sem_lotes_label = QLabel("❌ Nenhum lote disponível para venda")
            sem_lotes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sem_lotes_label.setStyleSheet("""
                QLabel {
                    color: #dc3545;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 30px;
                    background-color: #f8d7da;
                    border: 2px solid #f5c6cb;
                    border-radius: 8px;
                }
            """)
            self.layout_lotes.addWidget(sem_lotes_label)
            self.botao_comprar.setEnabled(False)
            return
            
        # Cria widget para cada lote
        for lote in lotes_disponiveis:
            widget_lote = self.criar_widget_lote(lote)
            self.layout_lotes.addWidget(widget_lote)
            self.lotes_widgets.append(widget_lote)
            
        # Adiciona espaçador para organizar melhor
        self.layout_lotes.addStretch()
        
        # Força atualização inicial do resumo
        self.atualizar_resumo()
        
    def criar_widget_lote(self, lote):
        """Cria o widget para um lote específico"""
        # Criar widget do lote simplificado
        lote_widget = LoteWidget(lote, self)
        
        return lote_widget
        
        
    def atualizar_resumo(self):
        """Atualiza o resumo da compra"""
        total_ingressos = 0
        valor_total = 0.0
        
        for widget in self.lotes_widgets:
            if isinstance(widget, LoteWidget):
                quantidade = widget.get_quantidade()
                total_ingressos += quantidade
                valor_total += widget.get_valor_total()
                
        self.label_total_ingressos.setText(str(total_ingressos))
        self.label_valor_total.setText(f"R$ {valor_total:.2f}")
        
        # Habilita/desabilita botão de comprar
        self.botao_comprar.setEnabled(total_ingressos > 0)
        
    def confirmar_compra(self):
        """Confirma e executa a compra"""
        # Coleta dados da compra
        compras = []
        for widget in self.lotes_widgets:
            if isinstance(widget, LoteWidget):
                quantidade = widget.get_quantidade()
                if quantidade > 0:
                    compras.append({
                        "lote_id": widget.lote_id,
                        "quantidade": quantidade,
                        "preco_unitario": widget.preco_unitario
                    })
                    
        if not compras:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um ingresso.")
            return
            
        # Calcular totais
        total_ingressos = sum(c["quantidade"] for c in compras)
        valor_total = sum(c["quantidade"] * c["preco_unitario"] for c in compras)
        
        # Criar texto de confirmação
        texto_lotes = []
        for compra in compras:
            # Encontrar nome do lote
            lote = next((l for l in self.lotes if l["id"] == compra["lote_id"]), None)
            if lote:
                texto_lotes.append(f"• {lote['name']}: {compra['quantidade']} ingresso(s) - R$ {compra['quantidade'] * compra['preco_unitario']:.2f}")
        
        texto_confirmacao = (
            f"Confirma a compra de {total_ingressos} ingresso(s)?\n\n"
            f"Evento: {self.dados_evento['name']}\n\n"
            f"Ingressos:\n" + "\n".join(texto_lotes) + 
            f"\nTotal: R$ {valor_total:.2f}"
        )
        
        reply = QMessageBox.question(
            self,
            "Confirmar Compra",
            texto_confirmacao,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            asyncio.create_task(self.executar_compra(compras))
            
    async def executar_compra(self, compras):
        """Executa a compra de forma assíncrona"""
        try:
            total_comprados = 0
            erros = []
            erro_autenticacao = False
            
            for compra in compras:
                dados_ingresso = {
                    "event_id": self.dados_evento["id"],
                    "quantity": compra["quantidade"],
                    "batch_id": compra["lote_id"]
                }
                
                resultado = await self.api_client.comprar_ingressos(dados_ingresso)
                
                if resultado["success"]:
                    total_comprados += len(resultado["tickets"])
                else:
                    # Verifica se é erro de autenticação
                    if "Unauthorized" in resultado["error"] or "Não autorizado" in resultado["error"]:
                        erro_autenticacao = True
                        break
                    
                    # Encontrar nome do lote para o erro
                    lote = next((l for l in self.lotes if l["id"] == compra["lote_id"]), None)
                    nome_lote = lote["name"] if lote else f"Lote {compra['lote_id']}"
                    erros.append(f"{nome_lote}: {resultado['error']}")
            
            # Se houve erro de autenticação, redireciona para login
            if erro_autenticacao:
                reply = QMessageBox.question(
                    self,
                    "Login Necessário",
                    "Você precisa estar logado para comprar ingressos.\n\n"
                    "Deseja fazer login agora?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Fecha o diálogo e permite que o usuário faça login
                    self.reject()
                else:
                    self.reject()
                return
            
            if total_comprados > 0:
                if erros:
                    # Compra parcial
                    QMessageBox.information(
                        self,
                        "Compra Parcial",
                        f"Compra parcialmente realizada!\n"
                        f"{total_comprados} ingresso(s) adquirido(s).\n\n"
                        f"Erros:\n" + "\n".join(erros) + "\n\n"
                        f"Você pode visualizar seus ingressos em 'Meus Ingressos'."
                    )
                else:
                    # Compra completa
                    QMessageBox.information(
                        self,
                        "Compra Realizada",
                        f"Compra realizada com sucesso!\n"
                        f"{total_comprados} ingresso(s) adquirido(s).\n\n"
                        f"Você pode visualizá-los em 'Meus Ingressos'."
                    )
                self.accept()
            else:
                # Nenhuma compra realizada
                QMessageBox.critical(
                    self, 
                    "Erro", 
                    f"Não foi possível realizar a compra:\n\n" + "\n".join(erros)
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")


class EventCard(QFrame):
    """Card individual para exibir um evento"""
    
    def __init__(self, dados_evento, api_client):
        super().__init__()
        self.dados_evento = dados_evento
        self.api_client = api_client
        self.setup_ui()
        self.setup_style()
        
    def setup_ui(self):
        """Configura a interface do card"""
        self.setFixedSize(280, 200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SIZES['spacing'], SIZES['spacing'], 
                                SIZES['spacing'], SIZES['spacing'])
        layout.setSpacing(SIZES['spacing_small'])
        
        # Nome do evento
        label_nome = QLabel(self.dados_evento["name"])
        font_nome = QFont()
        font_nome.setPointSize(FONTS['size_medium'])
        font_nome.setBold(True)
        label_nome.setFont(font_nome)
        label_nome.setWordWrap(True)
        label_nome.setMaximumHeight(40)
        layout.addWidget(label_nome)
        
        # Descrição
        label_desc = QLabel(self.dados_evento["description"])
        label_desc.setWordWrap(True)
        label_desc.setMaximumHeight(32)
        label_desc.setStyleSheet(f"color: {COLORS['text_light']};")
        layout.addWidget(label_desc)
        
        # Data e hora
        label_data_hora = QLabel(f"📅 {self.dados_evento['data']} às {self.dados_evento['hora']}")
        label_data_hora.setStyleSheet(f"font-size: {FONTS['size_small']}px;")
        layout.addWidget(label_data_hora)
        
        # Local
        label_local = QLabel(f"📍 {self.dados_evento['localizacao']}")
        label_local.setStyleSheet(f"font-size: {FONTS['size_small']}px;")
        layout.addWidget(label_local)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(SIZES['spacing_small'])
        
        # Botão de ver detalhes
        btn_detalhes = QPushButton("Ver Detalhes")
        btn_detalhes.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                font-weight: 600;
                padding: 4px 8px;
                font-size: {FONTS['size_small']}px;
                min-height: 28px;
                max-width: 90px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']}dd;
            }}
        """)
        btn_detalhes.clicked.connect(self.ver_detalhes)
        buttons_layout.addWidget(btn_detalhes)
        
        # Botão de comprar
        btn_comprar = QPushButton("Comprar")
        btn_comprar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: {COLORS['text_white']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                font-weight: 600;
                padding: 4px 8px;
                font-size: {FONTS['size_small']}px;
                min-height: 28px;
                max-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['success']}dd;
            }}
        """)
        btn_comprar.clicked.connect(self.comprar_ingresso)
        buttons_layout.addWidget(btn_comprar)
        
        layout.addLayout(buttons_layout)
        
    def setup_style(self):
        """Configura o estilo do card"""
        button_style_outline = get_button_stylesheet('outline')
        button_style_primary = get_button_stylesheet('primary')
        
        self.setStyleSheet(f"""
            EventCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {SIZES['border_radius']}px;
            }}
            EventCard:hover {{
                border-color: {COLORS['secondary']};
                background-color: {COLORS['surface_dark']};
            }}
            
            {button_style_outline}
            {button_style_primary}
        """)
        
    def ver_detalhes(self):
        """Abre o diálogo de detalhes do evento"""
        dialog = EventDetailsDialog(self.dados_evento, self.api_client, self)
        dialog.exec()
        
    def comprar_ingresso(self):
        """Abre o diálogo para compra de ingressos"""
        dialog = TicketPurchaseDialog(self.dados_evento, self.api_client, self)
        dialog.exec()


class CatalogWidget(QWidget):
    """Widget principal do catálogo de eventos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.eventos = []
        self.task_carregamento = None
        self.ja_carregou = False
        self.setup_ui()
        # Não carrega eventos no __init__ para evitar problemas com loop assíncrono
        
    def setup_ui(self):
        """Configura a interface do catálogo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SIZES['spacing_large'], SIZES['spacing_large'], 
                                SIZES['spacing_large'], SIZES['spacing_large'])
        layout.setSpacing(SIZES['spacing'])
        
        # Cabeçalho da página
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Catálogo de Eventos")
        title_font = QFont()
        title_font.setPointSize(FONTS['size_title'])
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {COLORS['primary']};")
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
        update_btn.clicked.connect(self.carregar_eventos)
        header_layout.addWidget(update_btn)
        
        layout.addLayout(header_layout)
        
        # Área de rolagem para os eventos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget do conteúdo dos eventos
        self.widget_eventos = QWidget()
        self.layout_eventos = QGridLayout(self.widget_eventos)
        self.layout_eventos.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_eventos.setSpacing(SIZES['spacing'])
        
        scroll_area.setWidget(self.widget_eventos)
        layout.addWidget(scroll_area)
        
        # Mensagem de carregamento
        self.loading_label = QLabel("Carregando eventos...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(f"color: {COLORS['text_light']};")
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
    def showEvent(self, event):
        """Chamado quando o widget se torna visível"""
        super().showEvent(event)
        if not self.ja_carregou:
            self.ja_carregou = True
            QTimer.singleShot(100, self.carregar_eventos)
        
    def carregar_eventos(self):
        """Carrega os eventos da API"""
        if self.task_carregamento and not self.task_carregamento.done():
            self.task_carregamento.cancel()
        self.loading_label.show()
        self.clear_events()
        self.task_carregamento = asyncio.create_task(self._async_carregar_eventos())
        
    async def _async_carregar_eventos(self):
        """Carrega os eventos de forma assíncrona (apenas eventos ativos)"""
        try:
            # Para o catálogo público, carregar apenas eventos ativos
            resultado = await self.api_client.get_eventos(active_only=True)
            
            if resultado["success"]:
                self.eventos = resultado["events"]
                self.exibir_eventos()
            else:
                # Verifica se é erro de conexão com a API
                error_msg = resultado['error']
                if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg or "Conexão recusada" in error_msg:
                    QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                else:
                    QMessageBox.critical(self, "Erro", f"Erro ao carregar eventos: {error_msg}")
        except Exception as e:
            error_str = str(e)
            if "Max retries exceeded" in error_str or "Failed to establish a new connection" in error_str or "Conexão recusada" in error_str:
                QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
            else:
                QMessageBox.critical(self, "Erro", f"Erro inesperado: {error_str}")
        finally:
            self.loading_label.hide()
            
    def exibir_eventos(self):
        """Exibe os eventos na grade"""
        row = 0
        col = 0
        max_cols = 3  # Máximo de 3 colunas
        
        for evento in self.eventos:
            card_evento = EventCard(evento, self.api_client)
            self.layout_eventos.addWidget(card_evento, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
    def clear_events(self):
        """Remove todos os eventos da grade"""
        while self.layout_eventos.count():
            child = self.layout_eventos.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
