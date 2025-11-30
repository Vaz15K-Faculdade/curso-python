from PySide6.QtWidgets import (QDialog, QVBoxLayout,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QGroupBox, QFormLayout,
                               QLineEdit, QSpinBox, QDoubleSpinBox,
                               QComboBox, QMessageBox, QDialogButtonBox)
from frontend.styles import get_button_stylesheet, get_dialog_stylesheet, get_table_stylesheet


class BatchCreationDialog(QDialog):
    """Diálogo para criar e gerenciar lotes de um novo evento."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.batches = []
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setWindowTitle("Configuração de Lotes de Ingressos")
        self.setMinimumSize(700, 500)
        self.setModal(True)
        self.setStyleSheet(get_dialog_stylesheet() + """
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 8px 2px 8px;
                background-color: #2c3e50;
                color: white;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Formulário para adicionar novo lote
        form_group = QGroupBox("Adicionar Novo Lote")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 25, 15, 15)

        self.batch_name_edit = QLineEdit()
        self.batch_name_edit.setPlaceholderText("Ex: 1º Lote, Lote Promocional")
        form_layout.addRow("Nome do Lote:", self.batch_name_edit)

        self.lote_number_spin = QSpinBox()
        self.lote_number_spin.setRange(1, 100)
        self.lote_number_spin.setValue(1)
        form_layout.addRow("Número do Lote:", self.lote_number_spin)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 10000)
        self.quantity_spin.setValue(100)
        form_layout.addRow("Quantidade:", self.quantity_spin)

        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.0, 9999.99)
        self.price_spin.setDecimals(2)
        self.price_spin.setValue(50.00)
        form_layout.addRow("Preço (R$):", self.price_spin)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["waiting", "active"])
        form_layout.addRow("Status:", self.status_combo)

        add_batch_btn = QPushButton("Adicionar Lote")
        add_batch_btn.setStyleSheet(get_button_stylesheet('primary'))
        add_batch_btn.clicked.connect(self.add_batch)
        form_layout.addRow(add_batch_btn)

        layout.addWidget(form_group)

        # Tabela de lotes adicionados
        batches_group = QGroupBox("Lotes Adicionados")
        batches_layout = QVBoxLayout(batches_group)

        self.tabela_lotes = QTableWidget()
        self.tabela_lotes.setColumnCount(5)
        self.tabela_lotes.setHorizontalHeaderLabels(["Nome", "Quantidade", "Preço", "Status", "Ações"])
        self.tabela_lotes.setStyleSheet(get_table_stylesheet())
        header = self.tabela_lotes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        batches_layout.addWidget(self.tabela_lotes)

        layout.addWidget(batches_group)

        # Botões de confirmação
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet(get_button_stylesheet('primary'))
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet(get_button_stylesheet('outline'))
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def add_batch(self):
        """Adiciona um novo lote à lista e à tabela."""
        name = self.batch_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Erro", "O nome do lote é obrigatório.")
            return

        dado_lote = {
            "name": name,
            "numero_lote": self.lote_number_spin.value(),
            "total_ingressos": self.quantity_spin.value(),
            "price": self.price_spin.value(),
            "status": self.status_combo.currentText()
        }

        self.batches.append(dado_lote)
        self.update_table()
        self.clear_form()

    def update_table(self):
        """Atualiza a tabela com os lotes da lista."""
        self.tabela_lotes.setRowCount(len(self.batches))
        for row, batch in enumerate(self.batches):
            self.tabela_lotes.setItem(row, 0, QTableWidgetItem(batch["name"]))
            self.tabela_lotes.setItem(row, 1, QTableWidgetItem(str(batch["total_ingressos"])))
            self.tabela_lotes.setItem(row, 2, QTableWidgetItem(f"R$ {batch['price']:.2f}"))
            self.tabela_lotes.setItem(row, 3, QTableWidgetItem(batch["status"]))

            # Botão de remover
            remove_btn = QPushButton("Remover")
            remove_btn.setStyleSheet(get_button_stylesheet('danger'))
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_batch(r))
            self.tabela_lotes.setCellWidget(row, 4, remove_btn)

    def remove_batch(self, row):
        """Remove um lote da lista."""
        if 0 <= row < len(self.batches):
            del self.batches[row]
            self.update_table()

    def clear_form(self):
        """Limpa o formulário de adicionar lote."""
        self.batch_name_edit.clear()
        self.quantity_spin.setValue(100)
        self.price_spin.setValue(50.00)
        self.status_combo.setCurrentIndex(0)

    def get_batches(self):
        """Retorna a lista de lotes configurados."""
        return self.batches

