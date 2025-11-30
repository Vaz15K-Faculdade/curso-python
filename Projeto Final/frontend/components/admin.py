from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame, QGridLayout,
                               QMessageBox, QTableWidget, QTableWidgetItem,
                               QHeaderView, QTabWidget, QGroupBox, QFormLayout,
                               QLineEdit, QSpinBox, QTextEdit, QComboBox, QDialog,
                               QCheckBox, QDialogButtonBox, QDoubleSpinBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from frontend.styles import COLORS, SIZES, FONTS, get_button_stylesheet, get_dialog_stylesheet
from frontend.components.lotes import BatchCreationDialog
from frontend.components.relatorios import ReportsWidget
import asyncio
import concurrent.futures


class BatchEditDialog(QDialog):
    """Diálogo para editar lotes de ingressos"""
    
    def __init__(self, batch, api_client, parent=None):
        super().__init__(parent)
        self.batch = batch
        self.api_client = api_client
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        self.setWindowTitle(f"Editar Lote: {self.batch['name']}")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Informações do lote (somente leitura)
        info_group = QGroupBox("Informações do Lote")
        info_layout = QFormLayout(info_group)
        
        info_layout.addRow("ID:", QLabel(str(self.batch["id"])))
        info_layout.addRow("Ingressos Vendidos:", QLabel(str(self.batch["ingressos_vendidos"])))
        info_layout.addRow("Ingressos Disponíveis:", QLabel(str(self.batch["ingressos_disponiveis"])))
        
        layout.addWidget(info_group)
        
        # Configurações editáveis
        edit_group = QGroupBox("Configurações")
        edit_layout = QFormLayout(edit_group)
        
        # Nome do lote
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.batch.get("name", ""))
        edit_layout.addRow("Nome:", self.name_edit)
        
        # Descrição
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlainText(self.batch.get("description") or "")
        edit_layout.addRow("Descrição:", self.description_edit)
        
        # Total de ingressos
        self.total_tickets_spin = QSpinBox()
        self.total_tickets_spin.setRange(1, 10000)
        self.total_tickets_spin.setValue(self.batch.get("total_ingressos", 100))
        edit_layout.addRow("Total de Ingressos:", self.total_tickets_spin)
        
        # Preço
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.0, 9999.99)
        self.price_spin.setDecimals(2)
        self.price_spin.setValue(float(self.batch.get("price", 0.0)))
        edit_layout.addRow("Preço (R$):", self.price_spin)
        
        # Status do lote
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "waiting",
            "active",
            "sold_out",
            "expired"
        ])
        
        # Definir o status atual
        current_status = self.batch.get("status", "waiting")
        index = self.status_combo.findText(current_status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
            
        edit_layout.addRow("Status:", self.status_combo)
        
        # Explicação dos status
        status_info = QLabel("""
        • waiting: Lote não disponível para venda
        • active: Lote disponível para venda
        • sold_out: Lote sem ingressos disponíveis
        • expired: Lote expirado
        """)
        status_info.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        edit_layout.addRow("", status_info)
        
        # Ativo/Inativo
        self.active_checkbox = QCheckBox()
        self.active_checkbox.setChecked(self.batch.get("is_active", True))
        edit_layout.addRow("Lote Ativo:", self.active_checkbox)
        
        layout.addWidget(edit_group)
        
        # Botões
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_changes)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def save_changes(self):
        """Salva as alterações do lote"""
        # Cria os dados para atualização
        update_data = {
            "name": self.name_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip() or None,
            "total_ingressos": self.total_tickets_spin.value(),
            "price": float(self.price_spin.value()),
            "status": self.status_combo.currentText(),
            "is_active": self.active_checkbox.isChecked()
        }
        
        # Executa a atualização de forma assíncrona
        asyncio.create_task(self._async_save_changes(update_data))
        
    async def _async_save_changes(self, update_data):
        """Salva as alterações de forma assíncrona"""
        try:
            # Chama a API para atualizar o lote
            result = await self.api_client.atualizar_lote_ingresso(self.batch["id"], update_data)
            
            if result["success"]:
                QMessageBox.information(self, "Sucesso", "Lote atualizado com sucesso!")
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar lote: {result['error']}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")


class EventEditDialog(QDialog):
    """Diálogo para editar eventos com interface aprimorada"""
    
    def __init__(self, event_data, api_client, parent=None):
        super().__init__(parent)
        self.event_data = event_data
        self.api_client = api_client
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do diálogo de edição"""
        self.setWindowTitle(f"Editar Evento - {self.event_data['name']}")
        self.setFixedSize(650, 600)
        self.setModal(True)
        
        # Estilo geral do diálogo
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['surface_dark']}, stop:1 {COLORS['border_light']});
            }}
            QGroupBox {{
                font-weight: bold;
                font-size: {FONTS['size_normal']}px;
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['border_radius']}px;
                margin-top: {SIZES['spacing_small']}px;
                padding: {SIZES['spacing_small']}px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 8px 2px 8px;
                background-color: {COLORS['primary']};
                color: {COLORS['text_white']};
                border-radius: {SIZES['border_radius_small']}px;
            }}
            QLineEdit, QTextEdit {{
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['border_radius_small']}px;
                padding: {SIZES['spacing_small']}px;
                font-size: {FONTS['size_normal']}px;
                background-color: {COLORS['surface']};
                color: {COLORS['text']};
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {COLORS['secondary']};
            }}
            QCheckBox {{
                font-size: {FONTS['size_normal']}px;
                spacing: {SIZES['spacing_small']}px;
                color: {COLORS['text']};
            }}
        """)
        
        # Scroll area para o conteúdo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f1f3f4;
                border: none;
                border-radius: 6px;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #c1c8cd;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a8b2b9;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Formulário de edição
        form_group = QGroupBox("✏️ Informações do Evento")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(15, 15, 15, 15)
        
        # Nome do evento
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.event_data.get("name", ""))
        self.name_edit.setPlaceholderText("Nome do evento")
        form_layout.addRow("📝 Nome:", self.name_edit)
        
        # Descrição
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlainText(self.event_data.get("description", "") or "")
        self.description_edit.setPlaceholderText("Descrição do evento")
        form_layout.addRow("📋 Descrição:", self.description_edit)
        
        # Local
        self.location_edit = QLineEdit()
        self.location_edit.setText(self.event_data.get("localizacao", ""))
        self.location_edit.setPlaceholderText("Local do evento")
        form_layout.addRow("📍 Local:", self.location_edit)
        
        # Data
        self.date_edit = QLineEdit()
        self.date_edit.setText(self.event_data.get("data", ""))
        self.date_edit.setPlaceholderText("AAAA-MM-DD (ex: 2025-12-31)")
        form_layout.addRow("📅 Data:", self.date_edit)
        
        # Horário
        self.time_edit = QLineEdit()
        self.time_edit.setText(self.event_data.get("hora", ""))
        self.time_edit.setPlaceholderText("HH:MM (ex: 20:00)")
        form_layout.addRow("🕐 Horário:", self.time_edit)
        
        # Preço
        self.price_edit = QLineEdit()
        self.price_edit.setText(str(self.event_data.get("preco", 0.0)))
        self.price_edit.setPlaceholderText("0.00")
        form_layout.addRow("💰 Preço Base:", self.price_edit)
        
        # URL da imagem
        self.image_url_edit = QLineEdit()
        self.image_url_edit.setText(self.event_data.get("url_imagem", "") or "")
        self.image_url_edit.setPlaceholderText("https://exemplo.com/imagem.jpg (opcional)")
        form_layout.addRow("🖼️ URL da Imagem:", self.image_url_edit)
        
        # Status ativo
        self.active_checkbox = QCheckBox("Evento Ativo")
        self.active_checkbox.setChecked(self.event_data.get("ativo", True))
        form_layout.addRow("✅ Status:", self.active_checkbox)
        
        layout.addWidget(form_group)
        
        # Informações adicionais (somente leitura)
        info_group = QGroupBox("ℹ️ Informações do Sistema")
        info_layout = QFormLayout(info_group)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        # Data de criação
        created_label = QLabel(self.event_data.get("criado_em", "N/A"))
        created_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        info_layout.addRow("Data de Criação:", created_label)
        
        # Data de atualização
        updated_label = QLabel(self.event_data.get("atualizado_em", "N/A"))
        updated_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        info_layout.addRow("Última Atualização:", updated_label)
        
        layout.addWidget(info_group)
        
        # Configurar scroll
        scroll.setWidget(content_widget)
        
        # Layout principal do diálogo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(20, 10, 20, 20)
        buttons_layout.setSpacing(10)
        
        # Botão salvar
        save_btn = QPushButton("💾 Salvar Alterações")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: {COLORS['text_white']};
                border: none;
                padding: {SIZES['spacing']}px {SIZES['spacing_large']}px;
                border-radius: {SIZES['border_radius']}px;
                font-size: {FONTS['size_normal']}px;
                font-weight: bold;
                min-height: {SIZES['button_height']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['success']}dd;
            }}
            QPushButton:pressed {{
                background-color: {COLORS['success']}bb;
            }}
        """)
        save_btn.clicked.connect(self.save_event)
        buttons_layout.addWidget(save_btn)
        
        # Botão cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['border']};
                color: {COLORS['text']};
                border: none;
                padding: {SIZES['spacing']}px {SIZES['spacing_large']}px;
                border-radius: {SIZES['border_radius']}px;
                font-size: {FONTS['size_normal']}px;
                font-weight: bold;
                min-height: {SIZES['button_height']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['border_light']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['disabled']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(buttons_layout)
        
    def save_event(self):
        """Salva as alterações do evento"""
        # Validações básicas
        name = self.name_edit.text().strip()
        location = self.location_edit.text().strip()
        date = self.date_edit.text().strip()
        time = self.time_edit.text().strip()
        price_text = self.price_edit.text().strip()
        
        if not all([name, location, date, time, price_text]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return
        
        # Validar formato da data
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            QMessageBox.warning(self, "Erro", "Data deve estar no formato AAAA-MM-DD (ex: 2025-12-31).")
            return
        
        # Validar formato do horário
        try:
            datetime.strptime(time, '%H:%M')
        except ValueError:
            QMessageBox.warning(self, "Erro", "Horário deve estar no formato HH:MM (ex: 20:00).")
            return
        
        # Validar preço
        try:
            price = float(price_text.replace(',', '.'))
            if price < 0:
                raise ValueError("Preço não pode ser negativo")
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço deve ser um número válido (use . como separador decimal).")
            return
        
        # Preparar dados para atualização
        update_data = {
            "name": name,
            "description": self.description_edit.toPlainText().strip() or None,
            "localizacao": location,
            "data": date,
            "hora": time,
            "preco": price,
            "url_imagem": self.image_url_edit.text().strip() or None,
            "ativo": self.active_checkbox.isChecked()
        }
        
        # Confirmar alterações
        reply = QMessageBox.question(
            self,
            "Confirmar Alterações",
            f"Confirma as alterações no evento '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Usar uma abordagem mais segura para evitar conflitos de asyncio
            self._save_update_data = update_data
            QTimer.singleShot(100, self._delayed_save)
    
    def _delayed_save(self):
        """Executa o salvamento com delay para evitar conflitos"""
        # Criar um novo loop para esta operação
        def run_save():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.api_client.atualizar_evento(self.event_data["id"], self._save_update_data)
                )
                # Usar QTimer para atualizar a UI no thread principal
                QTimer.singleShot(0, lambda: self._handle_save_result(result))
            except Exception as e:
                QTimer.singleShot(0, lambda: self._handle_save_error(str(e)))
            finally:
                loop.close()
        
        # Executar em thread separado
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(run_save)
    
    def _handle_save_result(self, result):
        """Manipula o resultado do salvamento na UI thread"""
        print(f"Resultado do salvamento: {result}")
        if result["success"]:
            print(f"Evento atualizado - Status ativo: {result.get('event', {}).get('ativo', 'N/A')}")
            QMessageBox.information(self, "Sucesso", "Evento atualizado com sucesso!")
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar evento: {result['error']}")
    
    def _handle_save_error(self, error_message):
        """Manipula erros de salvamento na UI thread"""
        QMessageBox.critical(self, "Erro", f"Erro inesperado: {error_message}")


class UserEditDialog(QDialog):
    """Diálogo para editar permissões e status do usuário"""
    
    def __init__(self, user, api_client, parent=None):
        super().__init__(parent)
        self.user = user
        self.api_client = api_client
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        self.setWindowTitle(f"Editar Usuário: {self.user['email']}")
        self.setFixedSize(400, 300)
        self.setModal(True)
        self.setStyleSheet(get_dialog_stylesheet())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Informações do usuário (somente leitura)
        info_group = QGroupBox("Informações do Usuário")
        info_layout = QFormLayout(info_group)
        
        info_layout.addRow("ID:", QLabel(str(self.user["id"])))
        info_layout.addRow("Email:", QLabel(self.user["email"]))
        if self.user.get("cpf"):
            info_layout.addRow("CPF:", QLabel(self.user["cpf"]))
        if self.user.get("telefone"):
            info_layout.addRow("Telefone:", QLabel(self.user["telefone"]))
        
        layout.addWidget(info_group)
        
        # Configurações editáveis
        edit_group = QGroupBox("Configurações")
        edit_layout = QFormLayout(edit_group)
        
        # Status ativo/inativo
        self.active_checkbox = QCheckBox()
        self.active_checkbox.setChecked(self.user.get("is_active", True))
        edit_layout.addRow("Usuário Ativo:", self.active_checkbox)
        
        # Permissões
        self.permission_combo = QComboBox()
        self.permission_combo.addItems(["Cliente", "Operador", "Administrador"])
        
        # Define a permissão atual
        if self.user.get("is_superuser"):
            self.permission_combo.setCurrentText("Administrador")
        elif self.user.get("is_operator"):
            self.permission_combo.setCurrentText("Operador")
        else:
            self.permission_combo.setCurrentText("Cliente")
            
        edit_layout.addRow("Permissões:", self.permission_combo)
        
        layout.addWidget(edit_group)
        
        # Botões
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet(get_button_stylesheet('primary'))
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet(get_button_stylesheet('outline'))
        button_box.accepted.connect(self.save_changes)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def save_changes(self):
        """Salva as alterações do usuário"""
        # Determina as novas permissões
        permission = self.permission_combo.currentText()
        is_superuser = permission == "Administrador"
        is_operator = permission == "Operador"
        is_active = self.active_checkbox.isChecked()
        
        # Cria os dados para atualização
        update_data = {
            "is_active": is_active,
            "is_superuser": is_superuser,
            "is_operator": is_operator,
            "data_nascimento": self.user.get("data_nascimento"),
            "telefone": self.user.get("telefone"),
            "cpf": self.user.get("cpf")
        }
        
        # Executa a atualização de forma assíncrona
        asyncio.create_task(self._async_save_changes(update_data))
        
    async def _async_save_changes(self, update_data):
        """Salva as alterações de forma assíncrona"""
        try:
            # Chama a API real para atualizar o usuário
            result = await self.api_client.atualizar_usuario(self.user["id"], update_data)
            
            if result["success"]:
                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Usuário atualizado com sucesso!"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Erro ao atualizar usuário: {result['error']}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro inesperado: {str(e)}"
            )


class UserCard(QFrame):
    """Card para exibir informações de um usuário."""
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.parent_widget = parent
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("user_card")
        self.setFixedSize(200, 150)
        self.setStyleSheet(f"""
            QFrame#user_card {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: {SIZES['border_radius']}px;
            }}
            QFrame#user_card:hover {{
                border: 1px solid {COLORS['primary']};
            }}
        """)
        layout = QVBoxLayout(self)

        email_label = QLabel(self.user['email'])
        email_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(email_label)

        if self.user.get("is_superuser"):
            user_type = "Administrador"
        elif self.user.get("is_operator"):
            user_type = "Operador"
        else:
            user_type = "Cliente"

        permission_label = QLabel(f"Permissão: {user_type}")
        layout.addWidget(permission_label)

        status = "Ativo" if self.user.get("is_active") else "Inativo"
        status_label = QLabel(f"Status: {status}")
        layout.addWidget(status_label)
        # Botão de editar usuário (dentro do card)
        edit_btn = QPushButton("✏️")
        edit_btn.setStyleSheet(get_button_stylesheet('secondary'))
        edit_btn.clicked.connect(self.edit_user)
        layout.addWidget(edit_btn)

    def edit_user(self):
        dialog = UserEditDialog(self.user, self.parent_widget.api_client, self.parent_widget)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.parent_widget.carregar_users()

class UserManagementWidget(QWidget):
    """Widget para gerenciamento de usuários"""

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.users = []
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface de gerenciamento de usuários"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title_label = QLabel("Gerenciamento de Usuários")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Controles de filtro e pesquisa
        controls_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar por email ou CPF...")
        self.search_input.textChanged.connect(self.filtro_user)
        controls_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Todos", "Clientes", "Operadores", "Administradores", "Ativos", "Inativos"])
        self.filter_combo.currentIndexChanged.connect(self.filtro_user)
        controls_layout.addWidget(self.filter_combo)

        # Adiciona o botão de recarregar à direita do filtro
        self.update_btn = QPushButton("🔄")
        self.update_btn.setToolTip("Recarregar")
        self.update_btn.setStyleSheet(get_button_stylesheet('primary'))
        self.update_btn.clicked.connect(self.carregar_users)
        controls_layout.addWidget(self.update_btn)

        layout.addLayout(controls_layout)

        # Scroll area para os cards de usuário
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.users_widget = QWidget()
        self.users_layout = QGridLayout(self.users_widget)
        # Alinhar os cards à esquerda e ao topo (sem centralização)
        self.users_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.users_widget)
        layout.addWidget(self.scroll_area)

        # Mensagem de carregamento
        self.loading_label = QLabel("Carregando usuários...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

    def carregar_users(self):
        """Carrega a lista de usuários"""
        self.loading_label.show()
        asyncio.create_task(self._async_carregar_users())

    async def _async_carregar_users(self):
        """Carrega usuários de forma assíncrona"""
        try:
            result = await self.api_client.get_todos_usuarios()

            if result.get("success"):
                self.users = result.get("users", [])
                self.display_users()
            else:
                # Verifica se é erro de conexão com a API
                error_msg = result.get('error', '')
                if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg or "Conexão recusada" in error_msg:
                    QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                else:
                    QMessageBox.critical(self, "Erro", f"Erro ao carregar usuários: {error_msg}")

        except Exception as e:
            error_str = str(e)
            if "Max retries exceeded" in error_str or "Failed to establish a new connection" in error_str or "Conexão recusada" in error_str:
                QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar usuários: {error_str}")
        finally:
            self.loading_label.hide()

    def display_users(self):
        """Exibe os usuários na grade de cards"""
        # Limpa o layout antigo
        for i in reversed(range(self.users_layout.count())):
            widget = self.users_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        row = 0
        col = 0
        for user in self.users:
            card = UserCard(user, self)
            self.users_layout.addWidget(card, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def filtro_user(self):
        """Filtra os usuários com base na pesquisa e no filtro selecionado."""
        search_text = self.search_input.text().lower()
        filter_type = self.filter_combo.currentText()

        for i in range(self.users_layout.count()):
            item = self.users_layout.itemAt(i)
            if not item:
                continue
            card = item.widget()
            if not card:
                continue
            user = card.user

            # Filtro por tipo de usuário
            if filter_type == "Clientes" and (user.get('is_superuser') or user.get('is_operator')):
                card.hide()
                continue
            if filter_type == "Operadores" and not user.get('is_operator'):
                card.hide()
                continue
            if filter_type == "Administradores" and not user.get('is_superuser'):
                card.hide()
                continue
            if filter_type == "Ativos" and not user.get('is_active'):
                card.hide()
                continue
            if filter_type == "Inativos" and user.get('is_active'):
                card.hide()
                continue

            # Filtro por texto de pesquisa
            if search_text:
                if search_text not in user['email'].lower() and search_text not in user.get('cpf', '').lower():
                    card.hide()
                    continue

            card.show()

    def edit_user_dialog(self, user):
        """Abre o diálogo para editar permissões e status do usuário"""
        dialog = UserEditDialog(user, self.api_client, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Recarrega a lista de usuários após edição
            self.carregar_users()

class EventManagementWidget(QWidget):
    """Widget para gerenciamento de eventos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.task_carregamento = None
        self.ja_carregou = False
        self.batches = []
        self.setup_ui()
        # Carregar eventos apenas quando o widget se tornar visível
        
    def setup_ui(self):
        """Configura a interface de gerenciamento de eventos"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        title_label = QLabel("Gerenciamento de Eventos")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Formulário para criar/editar evento
        form_group = QGroupBox("Novo Evento")
        form_layout = QVBoxLayout(form_group)
        
        # Informações básicas do evento
        basic_info_group = QGroupBox("Informações Básicas")
        basic_layout = QFormLayout(basic_info_group)
        
        self.event_name = QLineEdit()
        self.event_name.setPlaceholderText("Nome do evento")
        basic_layout.addRow("Nome:", self.event_name)
        
        self.event_description = QTextEdit()
        self.event_description.setMaximumHeight(60)
        self.event_description.setPlaceholderText("Descrição do evento")
        basic_layout.addRow("Descrição:", self.event_description)
        
        self.event_location = QLineEdit()
        self.event_location.setPlaceholderText("Local do evento")
        basic_layout.addRow("Local:", self.event_location)
        
        # Data e horário em uma linha
        datetime_layout = QHBoxLayout()
        self.event_date = QLineEdit()
        self.event_date.setPlaceholderText("AAAA-MM-DD")
        datetime_layout.addWidget(self.event_date)
        
        self.event_time = QLineEdit()
        self.event_time.setPlaceholderText("HH:MM")
        datetime_layout.addWidget(self.event_time)
        
        basic_layout.addRow("Data e Horário:", datetime_layout)
        form_layout.addWidget(basic_info_group)
        
        # Botão para configurar lotes
        self.config_lotes_btn = QPushButton("Configurar Lotes de Ingressos")
        self.config_lotes_btn.setStyleSheet(get_button_stylesheet('secondary'))
        self.config_lotes_btn.clicked.connect(self.open_batch_config)
        form_layout.addWidget(self.config_lotes_btn)
        
        # Botões do formulário
        form_buttons = QHBoxLayout()
        
        criar_btn = QPushButton("Criar Evento")
        criar_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
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
                background-color: {COLORS['primary']}dd;
            }}
        """)
        criar_btn.clicked.connect(lambda: asyncio.create_task(self.create_event_with_batches()))
        form_buttons.addWidget(criar_btn)
        
        limpar_btn = QPushButton("Limpar")
        limpar_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['border']};
                color: {COLORS['text']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                font-weight: 600;
                padding: 4px 8px;
                font-size: {FONTS['size_small']}px;
                min-height: 28px;
                max-width: 70px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['border']}dd;
            }}
        """)
        limpar_btn.clicked.connect(self.clear_form)
        form_buttons.addWidget(limpar_btn)
        
        form_buttons.addStretch()
        form_layout.addLayout(form_buttons)
        
        layout.addWidget(form_group)
        
        # Lista de eventos existentes
        grupo_eventos = QGroupBox("Eventos Existentes")
        self.events_layout = QVBoxLayout(grupo_eventos)

        # Cabeçalho com título e botão de recarregar
        header_layout = QHBoxLayout()

        # Campo de pesquisa expansível à esquerda do botão de recarregar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar por nome do evento...")
        self.search_input.textChanged.connect(self.filter_events)
        # Permitir que o campo ocupe o máximo de espaço até o botão de recarregar
        from PySide6.QtWidgets import QSizePolicy
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header_layout.addWidget(self.search_input)

        # Botão para recarregar eventos (lado direito)
        update_btn = QPushButton("🔄")
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

        self.events_layout.addLayout(header_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.events_widget = QWidget()
        self.events_cards_layout = QGridLayout(self.events_widget)
        # Alinhar os cards à esquerda e ao topo (comportamento similar ao catálogo)
        self.events_cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.events_widget)
        self.events_layout.addWidget(self.scroll_area)
        layout.addWidget(grupo_eventos)
        
    def showEvent(self, event):
        """Chamado quando o widget se torna visível"""
        super().showEvent(event)
        if not self.ja_carregou:
            self.ja_carregou = True
            QTimer.singleShot(100, self.carregar_eventos)
        
    def open_batch_config(self):
        """Abre o diálogo de configuração de lotes."""
        dialog = BatchCreationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.batches = dialog.get_batches()
            QMessageBox.information(self, "Lotes Configurados", f"{len(self.batches)} lote(s) configurado(s) com sucesso.")

    async def create_event(self):
        """Cria um novo evento (método antigo mantido para compatibilidade)"""
        await self.create_event_with_batches()
    
    async def create_event_with_batches(self):
        """Cria um novo evento com os lotes configurados"""
        name = self.event_name.text().strip()
        description = self.event_description.toPlainText().strip()
        location = self.event_location.text().strip()
        date = self.event_date.text().strip()
        time = self.event_time.text().strip()
        
        if not all([name, location, date, time]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios (Nome, Local, Data, Horário).")
            return
            
        # Validar formato da data
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            QMessageBox.warning(self, "Erro", "Data deve estar no formato AAAA-MM-DD (ex: 2025-12-31).")
            return
            
        # Validar formato do horário
        try:
            datetime.strptime(time, '%H:%M')
        except ValueError:
            QMessageBox.warning(self, "Erro", "Horário deve estar no formato HH:MM (ex: 20:00).")
            return
        
        # Coletar dados dos lotes
        dados_lotes = self.batches
        
        if not dados_lotes:
            QMessageBox.warning(self, "Erro", "Configure pelo menos um lote de ingressos.")
            return
        
        # Dados do evento
        event_data = {
            "name": name,
            "description": description or None,
            "localizacao": location,
            "data": date,
            "hora": time,
            "preco": dados_lotes[0]["price"]  # Preço do primeiro lote como preço base
        }
        
        try:
            # Criar o evento
            result = await self.api_client.criar_evento(event_data)
            
            if result["success"]:
                event_id = result["event"]["id"]
                
                # Criar os lotes
                tudo_criado = True
                lotes_criados = []
                
                for dado_lote in dados_lotes:
                    dado_lote["event_id"] = event_id
                    batch_result = await self.api_client.criar_lote_ingresso(dado_lote)
                    
                    if batch_result["success"]:
                        lotes_criados.append(batch_result["batch"])
                    else:
                        tudo_criado = False
                        QMessageBox.warning(self, "Aviso", 
                            f"Evento criado, mas erro ao criar lote '{dado_lote['name']}': {batch_result['error']}")
                
                if tudo_criado:
                    QMessageBox.information(self, "Sucesso", 
                        f"Evento '{name}' criado com {len(lotes_criados)} lote(s) de ingressos!")
                else:
                    QMessageBox.information(self, "Parcial", 
                        f"Evento '{name}' criado, mas alguns lotes tiveram problemas. "
                        "Você pode gerenciar os lotes clicando no botão 🎫 na tabela de eventos.")
                
                self.clear_form()
                await self._async_carregar_eventos()
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao criar evento: {result['error']}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
            
    def carregar_eventos(self):
        """Carrega a lista de eventos da API"""
        if self.task_carregamento and not self.task_carregamento.done():
            self.task_carregamento.cancel()
        self.task_carregamento = asyncio.create_task(self._async_carregar_eventos())
            
    async def _async_carregar_eventos(self):
        """Carrega a lista de eventos da API de forma assíncrona (incluindo inativos)"""
        try:
            # Para o admin, carregar todos os eventos (ativos e inativos)
            result = await self.api_client.get_eventos(active_only=False)
            
            if result["success"]:
                events = result["events"]
                # Limpa o layout antigo
                for i in reversed(range(self.events_cards_layout.count())):
                    self.events_cards_layout.itemAt(i).widget().setParent(None)

                row = 0
                col = 0
                for event in events:
                    card = QFrame()
                    card.setObjectName("event_card")
                    card.setFixedSize(200, 200)
                    card.setStyleSheet(f"""
                        QFrame#event_card {{
                            background-color: {COLORS['surface']};
                            border: 1px solid {COLORS['border']};
                            border-radius: {SIZES['border_radius']}px;
                        }}
                        QFrame#event_card:hover {{
                            border: 1px solid {COLORS['primary']};
                        }}
                    """)
                    layout = QVBoxLayout(card)

                    name_label = QLabel(event['name'])
                    name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                    layout.addWidget(name_label)

                    date_label = QLabel(f"Data: {event['data']} às {event['hora']}")
                    layout.addWidget(date_label)

                    location_label = QLabel(f"Local: {event['localizacao']}")
                    layout.addWidget(location_label)

                    price_label = QLabel(f"Preço: R$ {event['preco']:.2f}")
                    layout.addWidget(price_label)

                    status_icon = "🟢" if event.get("ativo", False) else "🔴"
                    status_label = QLabel(f"Status: {status_icon}")
                    layout.addWidget(status_label)

                    buttons_layout = QHBoxLayout()
                    edit_btn = QPushButton("✏️")
                    edit_btn.setToolTip("Editar")
                    edit_btn.setStyleSheet(get_button_stylesheet('primary'))
                    edit_btn.clicked.connect(lambda checked, e=event: self.edit_event(e))
                    buttons_layout.addWidget(edit_btn)

                    batches_btn = QPushButton("🎫")
                    batches_btn.setToolTip("Lotes")
                    batches_btn.setStyleSheet(get_button_stylesheet('secondary'))
                    batches_btn.clicked.connect(lambda checked, e=event: self.gerenciar_lotes(e))
                    buttons_layout.addWidget(batches_btn)

                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Remover")
                    delete_btn.setStyleSheet(get_button_stylesheet('danger'))
                    delete_btn.clicked.connect(lambda checked, e=event: asyncio.create_task(self.delete_event(e)))
                    buttons_layout.addWidget(delete_btn)

                    layout.addLayout(buttons_layout)
                    self.events_cards_layout.addWidget(card, row, col)
                    col += 1
                    if col == 3:
                        col = 0
                        row += 1
                    
            else:
                # Verifica se é erro de conexão com a API
                error_msg = result['error']
                if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg or "Conexão recusada" in error_msg:
                    QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                else:
                    QMessageBox.warning(self, "Erro", f"Erro ao carregar eventos: {error_msg}")
                
        except Exception as e:
            error_str = str(e)
            if "Max retries exceeded" in error_str or "Failed to establish a new connection" in error_str or "Conexão recusada" in error_str:
                QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
            else:
                QMessageBox.critical(self, "Erro", f"Erro inesperado ao carregar eventos: {error_str}")

    def filter_events(self):
        """Filtra os eventos com base na pesquisa."""
        search_text = self.search_input.text().lower()

        for i in range(self.events_cards_layout.count()):
            card = self.events_cards_layout.itemAt(i).widget()
            name_label = card.findChild(QLabel)
            if name_label:
                event_name = name_label.text().lower()
                if search_text not in event_name:
                    card.hide()
                else:
                    card.show()
            
    def edit_event(self, event):
        """Edita um evento existente"""
        dialog = EventEditDialog(event, self.api_client, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Recarregar eventos após edição usando QTimer
            QTimer.singleShot(100, self.carregar_eventos)
        
    async def delete_event(self, event):
        """Remove um evento"""
        reply = QMessageBox.question(
            self, 
            "Confirmar exclusão", 
            f"Tem certeza que deseja remover o evento '{event['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = await self.api_client.deletar_evento(event["id"])
                
                if result["success"]:
                    QMessageBox.information(self, "Sucesso", "Evento removido com sucesso!")
                    await self._async_carregar_eventos()
                else:
                    QMessageBox.critical(self, "Erro", f"Erro ao remover evento: {result['error']}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
        
    def gerenciar_lotes(self, event):
        """Abre o diálogo de gerenciamento de lotes"""
        dialog = BatchManagementDialog(event, self.api_client, self)
        dialog.exec()
        
    def clear_form(self):
        """Limpa o formulário"""
        self.event_name.clear()
        self.event_description.clear()
        self.event_location.clear()
        self.event_date.clear()
        self.event_time.clear()
        self.batches = []


class BatchManagementDialog(QDialog):
    """Diálogo para gerenciar lotes de ingressos de um evento"""
    
    def __init__(self, event_data, api_client, parent=None):
        super().__init__(parent)
        self.event_data = event_data
        self.api_client = api_client
        self.setup_ui()
        # Carregar lotes depois que a UI estiver pronta
        QTimer.singleShot(100, lambda: asyncio.create_task(self.load_batches()))
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        self.setWindowTitle(f"Gerenciar Lotes - {self.event_data['name']}")
        self.setFixedSize(800, 600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Informações do evento
        info_group = QGroupBox("Informações do Evento")
        info_layout = QFormLayout(info_group)
        
        info_layout.addRow("Nome:", QLabel(self.event_data["name"]))
        info_layout.addRow("Data:", QLabel(f"{self.event_data['data']} {self.event_data['hora']}"))
        info_layout.addRow("Local:", QLabel(self.event_data["localizacao"]))
        
        layout.addWidget(info_group)
        
        # Formulário para criar novo lote
        form_group = QGroupBox("Criar Novo Lote")
        form_layout = QFormLayout(form_group)
        
        self.batch_name = QLineEdit()
        self.batch_name.setPlaceholderText("Ex: 1º Lote, Lote Promocional")
        form_layout.addRow("Nome do Lote:", self.batch_name)
        
        self.decrição_lotes = QTextEdit()
        self.decrição_lotes.setMaximumHeight(60)
        self.decrição_lotes.setPlaceholderText("Descrição opcional")
        form_layout.addRow("Descrição:", self.decrição_lotes)
        
        self.total_tickets = QSpinBox()
        self.total_tickets.setRange(1, 10000)
        self.total_tickets.setValue(100)
        form_layout.addRow("Total de Ingressos:", self.total_tickets)
        
        self.preco_lote = QDoubleSpinBox()
        self.preco_lote.setRange(0.00, 99999.99)  # Permitir eventos gratuitos
        self.preco_lote.setDecimals(2)
        self.preco_lote.setSuffix(" R$")
        self.preco_lote.setValue(float(self.event_data.get("price", 0)))
        form_layout.addRow("Preço:", self.preco_lote)
        
        # Botões do formulário
        form_buttons = QHBoxLayout()
        
        criar_lote_btn = QPushButton("Criar Lote")
        criar_lote_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
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
                background-color: {COLORS['success']}dd;
            }}
        """)
        criar_lote_btn.clicked.connect(lambda: asyncio.create_task(self.create_batch()))
        form_buttons.addWidget(criar_lote_btn)
        
        limpar_lote_btn = QPushButton("Limpar")
        limpar_lote_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['border']};
                color: {COLORS['text']};
                border: none;
                border-radius: {SIZES['border_radius_small']}px;
                font-weight: 600;
                padding: 4px 8px;
                font-size: {FONTS['size_small']}px;
                min-height: 28px;
                max-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['border']}dd;
            }}
        """)
        limpar_lote_btn.clicked.connect(self.clear_batch_form)
        form_buttons.addWidget(limpar_lote_btn)
        
        form_buttons.addStretch()
        form_layout.addRow(form_buttons)
        
        layout.addWidget(form_group)
        
        # Lista de lotes existentes
        batches_group = QGroupBox("Lotes Existentes")
        batches_layout = QVBoxLayout(batches_group)
        
        # Botão para recarregar lotes
        atualizar_lote_btn = QPushButton("🔄 Recarregar")
        atualizar_lote_btn.setStyleSheet(f"""
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
        atualizar_lote_btn.clicked.connect(lambda: asyncio.create_task(self.load_batches()))
        batches_layout.addWidget(atualizar_lote_btn)
        
        self.tabela_lotes = QTableWidget()
        self.tabela_lotes.setColumnCount(7)
        self.tabela_lotes.setHorizontalHeaderLabels([
            "Nome", "Total", "Vendidos", "Disponível", "Preço", "Status", "Ações"
        ])
        
        # Desabilitar edição por duplo clique
        self.tabela_lotes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Configurar redimensionamento das colunas
        header = self.tabela_lotes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Nome
        
        batches_layout.addWidget(self.tabela_lotes)
        layout.addWidget(batches_group)
        
        # Botões do diálogo
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.close)
        layout.addWidget(button_box)
        
    async def load_batches(self):
        """Carrega os lotes do evento"""
        try:
            result = await self.api_client.get_lotes_evento(self.event_data["id"])
            
            if result["success"]:
                batches = result["batches"]
                self.tabela_lotes.setRowCount(len(batches))
                
                for row, batch in enumerate(batches):
                    # Nome
                    self.tabela_lotes.setItem(row, 0, QTableWidgetItem(batch["name"]))
                    
                    # Total de ingressos
                    self.tabela_lotes.setItem(row, 1, QTableWidgetItem(str(batch["total_ingressos"])))
                    
                    # Vendidos
                    self.tabela_lotes.setItem(row, 2, QTableWidgetItem(str(batch["ingressos_vendidos"])))
                    
                    # Disponível
                    self.tabela_lotes.setItem(row, 3, QTableWidgetItem(str(batch["ingressos_disponiveis"])))
                    
                    # Preço
                    price_text = f"R$ {batch['price']:.2f}"
                    self.tabela_lotes.setItem(row, 4, QTableWidgetItem(price_text))
                    
                    # Status
                    status_text = batch["status"]
                    self.tabela_lotes.setItem(row, 5, QTableWidgetItem(str(status_text)))
                    
                    # Ações
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(5, 5, 5, 5)
                    
                    edit_batch_btn = QPushButton("✏️")
                    edit_batch_btn.setFixedSize(25, 25)
                    edit_batch_btn.setToolTip("Editar lote")
                    edit_batch_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {COLORS['primary']};
                            color: {COLORS['text_white']};
                            border: none;
                            border-radius: {SIZES['border_radius_small']}px;
                            font-size: {FONTS['size_small']}px;
                        }}
                        QPushButton:hover {{
                            background-color: {COLORS['primary']}dd;
                        }}
                    """)
                    edit_batch_btn.clicked.connect(lambda checked, b=batch: self.edit_batch(b))
                    
                    delet_lote_btn = QPushButton("🗑️")
                    delet_lote_btn.setFixedSize(25, 25)
                    delet_lote_btn.setToolTip("Remover lote")
                    delet_lote_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {COLORS['error']};
                            color: {COLORS['text_white']};
                            border: none;
                            border-radius: {SIZES['border_radius_small']}px;
                            font-size: {FONTS['size_small']}px;
                        }}
                        QPushButton:hover {{
                            background-color: {COLORS['error']}dd;
                        }}
                    """)
                    delet_lote_btn.clicked.connect(lambda checked, b=batch: asyncio.create_task(self.delete_batch(b)))
                    
                    actions_layout.addWidget(edit_batch_btn)
                    actions_layout.addWidget(delet_lote_btn)
                    actions_layout.addStretch()
                    
                    self.tabela_lotes.setCellWidget(row, 6, actions_widget)
                    
                # Lotes carregados com sucesso
                    
            else:
                # Verifica se é erro de conexão com a API
                error_msg = result['error']
                if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg or "Conexão recusada" in error_msg:
                    QMessageBox.warning(self, "Erro de Conexão", "Não foi possível conectar-se à API, verifique se ela está online")
                else:
                    QMessageBox.warning(self, "Erro", f"Erro ao carregar lotes: {error_msg}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
            
    async def create_batch(self):
        """Cria um novo lote"""
        numero_lote = self.tabela_lotes.rowCount() + 1
        dado_lote = {
            "event_id": self.event_data["id"],
            "name": self.batch_name.text().strip(),
            "numero_lote": numero_lote,
            "description": self.decrição_lotes.toPlainText().strip() or None,
            "total_ingressos": self.total_tickets.value(),
            "price": float(self.preco_lote.value())
        }
        
        if not dado_lote["name"]:
            QMessageBox.warning(self, "Erro", "Nome do lote é obrigatório.")
            return
        
        try:
            result = await self.api_client.criar_lote_ingresso(dado_lote)
            
            if result["success"]:
                QMessageBox.information(self, "Sucesso", f"Lote '{dado_lote['name']}' criado com sucesso!")
                self.clear_batch_form()
                await self.load_batches()
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao criar lote: {result['error']}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
            
    def edit_batch(self, batch):
        """Edita um lote"""
        dialog = BatchEditDialog(batch, self.api_client, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Recarregar lotes após edição
            asyncio.create_task(self.load_batches())
        
    async def delete_batch(self, batch):
        """Remove um lote"""
        reply = QMessageBox.question(
            self, 
            "Confirmar exclusão", 
            f"Tem certeza que deseja remover o lote '{batch['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = await self.api_client.deletar_lote_ingresso(batch["id"])
                
                if result["success"]:
                    QMessageBox.information(self, "Sucesso", "Lote removido com sucesso!")
                    await self.load_batches()
                else:
                    QMessageBox.critical(self, "Erro", f"Erro ao remover lote: {result['error']}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
                
    def clear_batch_form(self):
        """Limpa o formulário de lote"""
        self.batch_name.clear()
        self.decrição_lotes.clear()
        self.total_tickets.setValue(100)
        self.preco_lote.setValue(float(self.event_data.get("price", 0)))



class AdminWidget(QWidget):
    """Widget principal da área de administração"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface de administração"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Cabeçalho da administração
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 10)
        
        title_label = QLabel("🔧 Área de Administração")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Abas da administração
        self.tab_widget = QTabWidget()
        
        # Aba: Usuários
        self.user_management = UserManagementWidget(self.api_client)
        self.tab_widget.addTab(self.user_management, "👥 Usuários")
        
        # Aba: Eventos
        self.event_management = EventManagementWidget(self.api_client)
        self.tab_widget.addTab(self.event_management, "📅 Eventos")
        
        # Aba: Relatórios
        self.reports = ReportsWidget(self.api_client)
        self.tab_widget.addTab(self.reports, "📊 Relatórios")
        
        layout.addWidget(self.tab_widget)
        
    def load_initial_data(self):
        """Carrega dados iniciais da administração"""
        # Carrega usuários na primeira aba
        QTimer.singleShot(100, self.user_management.carregar_users)
        # Carrega dados do relatório
        QTimer.singleShot(200, self.reports.load_report_data)
