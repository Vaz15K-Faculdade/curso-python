from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame, QGridLayout,
                               QMessageBox, QGroupBox, QProgressBar, QSplitter)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QFont
from frontend.styles import COLORS, get_button_stylesheet
import asyncio


class ReportsWorker(QThread):
    """Worker thread para carregar dados dos relatórios"""
    
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
    def run(self):
        """Executa o carregamento dos dados em background"""
        try:
            # Criar loop de eventos para as chamadas assíncronas
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Carregar dados
            result = loop.run_until_complete(self._load_report_data())
            loop.close()
            
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))
    
    async def _load_report_data(self):
        """Carrega todos os dados necessários para os relatórios"""
        report_data = {
            "total_users": 0,
            "total_events": 0,
            "total_tickets_sold": 0,
            "total_revenue": 0.0,
            "events_data": [],
            "users_data": []
        }
        
        # Carregar usuários
        users_result = await self.api_client.get_todos_usuarios()
        if users_result["success"]:
            users = users_result["users"]
            report_data["total_users"] = len(users)
            report_data["users_data"] = users
        
        # Carregar eventos
        events_result = await self.api_client.get_eventos(active_only=False)
        if events_result["success"]:
            events = events_result["events"]
            report_data["total_events"] = len(events)
            
            # Para cada evento, carregar dados detalhados
            for event in events:
                event_data = {
                    "id": event["id"],
                    "name": event["name"],
                    "data": event["data"],
                    "localizacao": event["localizacao"],
                    "ativo": event["ativo"],
                    "total_tickets": 0,
                    "tickets_sold": 0,
                    "revenue": 0.0,
                    "batches": []
                }
                
                # Carregar lotes do evento
                batches_result = await self.api_client.get_lotes_evento(event["id"])
                if batches_result["success"]:
                    batches = batches_result["batches"]
                    event_data["batches"] = batches
                    
                    # Calcular estatísticas do evento
                    for batch in batches:
                        event_data["total_tickets"] += batch.get("total_ingressos", 0)
                        event_data["tickets_sold"] += batch.get("ingressos_vendidos", 0)
                        event_data["revenue"] += batch.get("ingressos_vendidos", 0) * batch.get("price", 0.0)
                
                report_data["events_data"].append(event_data)
                report_data["total_tickets_sold"] += event_data["tickets_sold"]
                report_data["total_revenue"] += event_data["revenue"]
        
        return report_data


class ReportsWidget(QWidget):
    """Widget principal para relatórios administrativos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.report_data = None
        self.worker = None
        
        self.setup_ui()
        self.load_report_data()
        
    def setup_ui(self):
        """Configura a interface dos relatórios"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        title_label = QLabel("📊 Relatórios Administrativos")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Barra de progresso para carregamento
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminado
        layout.addWidget(self.progress_bar)
        
        # Splitter para dividir geral e individual
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Seção de relatório geral
        self.general_report = self.criar_secao_relatorio()
        splitter.addWidget(self.general_report)
        
        # Seção de relatório individual
        self.individual_report = self.criar_secao_relatorio_indivisual()
        splitter.addWidget(self.individual_report)
        
        # Configurar splitter
        splitter.setSizes([300, 500])
        layout.addWidget(splitter)
        
        # Botão de atualizar
        self.refresh_button = QPushButton("🔄 Atualizar Dados")
        self.refresh_button.setStyleSheet(get_button_stylesheet())
        self.refresh_button.clicked.connect(self.load_report_data)
        layout.addWidget(self.refresh_button)
        
    def criar_secao_relatorio(self):
        """Cria a seção de relatório geral"""
        group = QGroupBox("📈 Relatório Geral da Aplicação")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Grid para os cards de estatísticas
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(15)
        
        # Cards serão criados dinamicamente
        layout.addLayout(self.stats_grid)
        
        # Área de scroll para o grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)
        
        container_layout = QVBoxLayout()
        container_layout.addWidget(scroll_area)
        
        container = QWidget()
        container.setLayout(container_layout)
        
        return container
        
    def criar_secao_relatorio_indivisual(self):
        """Cria a seção de relatório individual por evento"""
        group = QGroupBox("🎯 Relatórios Individuais por Evento")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Área de scroll para os cards de eventos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.events_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_container)
        self.events_layout.setSpacing(10)
        
        scroll_area.setWidget(self.events_container)
        layout.addWidget(scroll_area)
        
        return group
        
    def criar_card_stat(self, title, value, color, icon=""):
        """Cria um card de estatística"""
        card = QFrame()
        card.setFixedSize(200, 120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                border: 1px solid {COLORS['border']};
            }}
            QLabel {{
                color: white;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        # Ícone e título
        header_layout = QHBoxLayout()
        
        if icon:
            icon_label = QLabel(icon)
            icon_font = QFont()
            icon_font.setPointSize(16)
            icon_label.setFont(icon_font)
            header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valor
        value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return card
        
    def criar_event_card(self, event_data):
        """Cria um card para relatório individual de evento"""
        card = QFrame()
        card.setFixedHeight(180)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
                padding: 10px;
            }}
            QLabel {{
                color: {COLORS['text']};
                border: none;
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Informações do evento
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # Nome do evento
        name_label = QLabel(f"📅 {event_data['name']}")
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_label.setFont(name_font)
        info_layout.addWidget(name_label)
        
        # Data e local
        date_label = QLabel(f"📍 {event_data['localizacao']} - {event_data['data']}")
        info_layout.addWidget(date_label)
        
        # Status
        status_text = "✅ Ativo" if event_data['ativo'] else "❌ Inativo"
        status_label = QLabel(status_text)
        status_color = COLORS['success'] if event_data['ativo'] else COLORS['error']
        status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
        info_layout.addWidget(status_label)
        
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Estatísticas
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)
        
        # Total de ingressos
        total_label = QLabel("🎫 Total:")
        total_label.setStyleSheet("font-weight: bold;")
        stats_layout.addWidget(total_label, 0, 0)
        
        total_value = QLabel(str(event_data['total_tickets']))
        total_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        stats_layout.addWidget(total_value, 0, 1)
        
        # Vendidos
        sold_label = QLabel("✅ Vendidos:")
        sold_label.setStyleSheet("font-weight: bold;")
        stats_layout.addWidget(sold_label, 1, 0)
        
        sold_value = QLabel(str(event_data['tickets_sold']))
        sold_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        stats_layout.addWidget(sold_value, 1, 1)
        
        # Receita
        revenue_label = QLabel("💰 Receita:")
        revenue_label.setStyleSheet("font-weight: bold;")
        stats_layout.addWidget(revenue_label, 2, 0)
        
        revenue_value = QLabel(f"R$ {event_data['revenue']:.2f}")
        revenue_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #007bff;")
        stats_layout.addWidget(revenue_value, 2, 1)
        
        # Disponíveis
        available = event_data['total_tickets'] - event_data['tickets_sold']
        available_label = QLabel("📦 Disponíveis:")
        available_label.setStyleSheet("font-weight: bold;")
        stats_layout.addWidget(available_label, 0, 2)
        
        available_value = QLabel(str(available))
        available_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #6c757d;")
        stats_layout.addWidget(available_value, 0, 3)
        
        # Taxa de ocupação
        if event_data['total_tickets'] > 0:
            occupancy_rate = (event_data['tickets_sold'] / event_data['total_tickets']) * 100
            occupancy_label = QLabel("📊 Ocupação:")
            occupancy_label.setStyleSheet("font-weight: bold;")
            stats_layout.addWidget(occupancy_label, 1, 2)
            
            occupancy_value = QLabel(f"{occupancy_rate:.1f}%")
            occupancy_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffc107;")
            stats_layout.addWidget(occupancy_value, 1, 3)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        return card
        
    def load_report_data(self):
        """Inicia o carregamento dos dados dos relatórios"""
        if self.worker and self.worker.isRunning():
            return
            
        self.progress_bar.setVisible(True)
        self.refresh_button.setEnabled(False)
        self.refresh_button.setText("⏳ Carregando...")
        
        # Limpar dados anteriores
        self.clear_current_data()
        
        # Iniciar worker
        self.worker = ReportsWorker(self.api_client)
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.error.connect(self.on_data_error)
        self.worker.start()
        
    def clear_current_data(self):
        """Limpa os dados atuais da interface"""
        # Limpar grid de estatísticas
        while self.stats_grid.count():
            child = self.stats_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Limpar cards de eventos
        while self.events_layout.count():
            child = self.events_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def on_data_loaded(self, data):
        """Callback quando os dados são carregados com sucesso"""
        self.report_data = data
        self.progress_bar.setVisible(False)
        self.refresh_button.setEnabled(True)
        self.refresh_button.setText("🔄 Atualizar Dados")
        
        # Atualizar interface com os dados
        self.atualizar_stats()
        self.atualizar_relatorio_individual()
        
    def on_data_error(self, error_message):
        """Callback quando ocorre erro no carregamento"""
        self.progress_bar.setVisible(False)
        self.refresh_button.setEnabled(True)
        self.refresh_button.setText("🔄 Atualizar Dados")
        
        # Verifica se é erro de conexão com a API
        if "Max retries exceeded" in error_message or "Failed to establish a new connection" in error_message or "Conexão recusada" in error_message:
            QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
        else:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados dos relatórios:\n{error_message}")
        
    def atualizar_stats(self):
        """Atualiza as estatísticas gerais"""
        if not self.report_data:
            return
            
        # Criar cards de estatísticas
        stats = [
            ("👥 Total de Usuários", self.report_data["total_users"], COLORS['primary']),
            ("📅 Total de Eventos", self.report_data["total_events"], COLORS['secondary']),
            ("🎫 Ingressos Vendidos", self.report_data["total_tickets_sold"], COLORS['success']),
            ("💰 Receita Total", f"R$ {self.report_data['total_revenue']:.2f}", COLORS['accent'])
        ]
        
        row, col = 0, 0
        for title, value, color in stats:
            card = self.criar_card_stat(title, value, color)
            self.stats_grid.addWidget(card, row, col)
            
            col += 1
            if col >= 4:  # 4 cards por linha
                col = 0
                row += 1
        
    def atualizar_relatorio_individual(self):
        """Atualiza os relatórios individuais por evento"""
        if not self.report_data:
            return
            
        # Criar cards para cada evento
        for event_data in self.report_data["events_data"]:
            event_card = self.criar_event_card(event_data)
            self.events_layout.addWidget(event_card)
        
        # Adicionar stretch no final
        self.events_layout.addStretch()
